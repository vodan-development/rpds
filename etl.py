"""
etl.py – FAIR-compliant RDF Export and AllegroGraph Upload
Models field reports with full provenance, spatial data, and semantic metadata.
Updated - April,2026 Aksum University Team
"""

import pandas as pd
import os
import requests
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, DCTERMS, PROV
from dotenv import load_dotenv; load_dotenv()

# ---------------------------------------------------------
# RDF NAMESPACES (Aligned with RPDSCDM.ttl)
# ---------------------------------------------------------
# Local Common Data Model Namespace
HDS = Namespace("http://example.org/hds#")
# Resource base for generating unique identifiers
BASE = Namespace("https://fieldlab1.example.org/resource/")
# Standard Geospatial vocabulary
GEO = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")

# ---------------------------------------------------------
# AllegroGraph Configuration (from .env)
# ---------------------------------------------------------

AG_SERVER_URL = os.getenv("AG_BASE_URL") 
AG_REPOSITORY = os.getenv("AG_REPO")
AG_USERNAME = os.getenv("AG_USER")     
AG_PASSWORD = os.getenv("AG_PASSWORD")

SPARQL_ENDPOINT = f"{AG_SERVER_URL}/repositories/{AG_REPOSITORY}/sparql"

# Define your Application CDM local path
CDM_PATH = "RPDSCDM.ttl" 


# ---------------------------------------------------------
# HELPER: LOAD LOCAL CDM
# ---------------------------------------------------------
def load_local_cdm():
    """Loads the local CDM into a reference graph."""
    if not os.path.exists(CDM_PATH):
        print(f"Warning: {CDM_PATH} not found. Using namespace only.")
        return None
    
    cdm_graph = Graph()
    cdm_graph.parse(CDM_PATH, format="turtle")
    print(f"Successfully loaded CDM with {len(cdm_graph)} triples.")
    return cdm_graph


# Add this helper function 
# Ensures a string can be converted to a valid ISO datetime; returns None if invalid
def safe_date_convert(val, is_datetime=True):
    """Ensures a string can be converted to a valid ISO datetime; returns None if invalid."""
    try:
        if pd.isna(val) or str(val).strip() == "":
            return None
        # This will fail for Feb 29 on non-leap years
        dt = pd.to_datetime(val)
        return dt.isoformat()
    except:
        return None


def dataframe_to_rdf(df: pd.DataFrame) -> bytes:
    # Transforms tabular case data into a FAIR-compliant Knowledge Graph
    # using the local HDS Common Data Model.
    g = Graph()

    # Normalize column names to lowercase and underscores
    df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]

    g.bind("hds", HDS)
    g.bind("res", BASE)
    g.bind("geo", GEO)
    g.bind("dct", DCTERMS)
    g.bind("prov", PROV)
 
    # --- HERE IS THE USE OF THE LOCAL CDM April 29 ,2026 ---
    cdm_ref = load_local_cdm()

    # Use an empty Graph as a fallback if the file is missing to avoid NoneType errors
    if cdm_ref is None:
      cdm_ref = Graph() 
      print("Warning: CDM reference is empty. Proceeding with default mapping.")
    else:
      print(f"Aligning data with {len(cdm_ref)} local CDM definitions.")

    # You can now use cdm_ref to validate classes or fetch labels
    # while building your export graph (g)

    for _, row in df.iterrows():
        # Create unique URIs for entities
        case_id = str(row["id"])
        incident_uri = BASE[f"incident/{case_id}"]
        record_uri = BASE[f"record/{case_id}"]
        victim_uri = BASE[f"victim/{case_id}"]
        perp_uri = BASE[f"perpetrator/{case_id}"]
        location_uri = BASE[f"location/{case_id}"]

        # --- A. RECORD & PROVENANCE ---
        # Logic: Check if hds:Record is defined in our CDM before using it
        if (HDS.Record, RDF.type, None) in cdm_ref or not cdm_ref:
            g.add((record_uri, RDF.type, HDS.Record))
            g.add((record_uri, HDS.reportsOn, incident_uri))
            
            if pd.notna(row.get("created_at")):
                valid_ts = safe_date_convert(row.get("created_at"), is_datetime=True)
                if valid_ts:
                  g.add((record_uri, HDS.recordedAt, Literal(valid_ts, datatype=XSD.dateTime)))
                #g.add((record_uri, HDS.recordedAt, Literal(row["created_at"], datatype=XSD.dateTime)))
            if pd.notna(row.get("input_by")):
                g.add((record_uri, HDS.inputBy, Literal(str(row["input_by"]))))

        # --- B. THE INCIDENT ---
        g.add((incident_uri, RDF.type, HDS.Incident))
        if pd.notna(row.get("event_type")):
            g.add((incident_uri, DCTERMS.type, Literal(row["event_type"])))
        if pd.notna(row.get("event_date")):
            valid_date = safe_date_convert(row.get("event_date"), is_datetime=False)
            if valid_date:
              g.add((incident_uri, DCTERMS.date, Literal(valid_date, datatype=XSD.date)))
            #g.add((incident_uri, DCTERMS.date, Literal(row["event_date"], datatype=XSD.date)))
        if pd.notna(row.get("time_range")):
            # Mapping from RPDSCDM: hds:timeRange
            g.add((incident_uri, HDS.timeRange, Literal(row["time_range"])))

        # --- C. VICTIM LINKING ---
        g.add((victim_uri, RDF.type, HDS.Victim))
        g.add((incident_uri, HDS.hasVictim, victim_uri))
        
        victim_info = []
        if pd.notna(row.get("ethnicity")): victim_info.append(f"Ethnicity: {row['ethnicity']}")
        if pd.notna(row.get("affected_status")): victim_info.append(f"Status: {row['affected_status']}")
        
        if victim_info:
            g.add((victim_uri, HDS.description, Literal("; ".join(victim_info))))

        # --- D. PERPETRATOR LINKING ---
        # Logic: Using hds:hasPerpetrator from CDM
        g.add((perp_uri, RDF.type, HDS.Perpetrator))
        g.add((incident_uri, HDS.hasPerpetrator, perp_uri))
        if pd.notna(row.get("affiliation")):
            g.add((perp_uri, HDS.description, Literal(row["affiliation"])))

        # --- E. LOCATION (Geospatial) ---
        g.add((location_uri, RDF.type, HDS.Camp))
        g.add((incident_uri, HDS.fromLocation, location_uri))
        
        if pd.notna(row.get("camp_name")):
            g.add((location_uri, RDFS.label, Literal(row["camp_name"])))
        
        # Adding Geo-coordinates for map visualization in AllegroGraph
        if pd.notna(row.get("latitude")) and row["latitude"] != 0:
            g.add((location_uri, GEO.lat, Literal(float(row["latitude"]), datatype=XSD.float)))
        if pd.notna(row.get("longitude")) and row["longitude"] != 0:
            g.add((location_uri, GEO.long, Literal(float(row["longitude"]), datatype=XSD.float)))

        # --- F. POLICY METADATA ---
        is_sens = True if row.get("is_sensitive") == 1 else False
        g.add((incident_uri, HDS.isSensitive, Literal(is_sens, datatype=XSD.boolean)))
        
        is_anon = True if row.get("is_anonymous") == 1 else False
        g.add((incident_uri, HDS.isAnonymous, Literal(is_anon, datatype=XSD.boolean)))

    # Return serialized turtle bytes for upload
    return g.serialize(format="turtle").encode("utf-8")

   
def upload_to_allegrograph(rdf_turtle: bytes):
    # Securely upload RDF data to AllegroGraph statements endpoint.
    endpoint = f"{AG_SERVER_URL}/repositories/{AG_REPOSITORY}/statements"
    headers = {"Content-Type": "text/turtle"}

    try:
        resp = requests.post(
            endpoint,
            data=rdf_turtle,
            headers=headers,
            auth=(AG_USERNAME, AG_PASSWORD),
            timeout=30,
        )
        if 200 <= resp.status_code < 300:
            return True, "Data successfully synchronized with Knowledge Graph."
        else:
            return False, f"AllegroGraph Error: {resp.status_code} - {resp.text}"
    except Exception as e:
        return False, f"Connection Failed: {str(e)}"