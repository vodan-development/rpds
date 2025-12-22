import streamlit as st
from datetime import date, datetime
import pandas as pd
import requests  # for SPARQL HTTP requests

from db import get_connection, init_db
from schema import LOCATION_REGISTRY, EVENT_TYPES, AFFECTED_STATUSES, LABELS
from etl import (
    dataframe_to_rdf,
    upload_to_allegrograph,
    SPARQL_ENDPOINT,
    AG_USERNAME,
    AG_PASSWORD,
)

# ---------------------------------------------------------
# BASIC APP CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="FieldLab1 UI Prototype", layout="wide")

# Ensure DB and table exist
init_db()

# ---------------------------------------------------------
# SIDEBAR: ROLE, LANGUAGE, PAGE
# ---------------------------------------------------------
st.sidebar.title("FieldLab1")

role = st.sidebar.selectbox(
    "Select your role",
    ["Field Worker", "Sector Officer", "Admin"],
    index=0,
)

language = st.sidebar.selectbox(
    "Language / ቋንቋ",
    ["English", "Amharic "],
    index=0,
)

page = st.sidebar.radio(
    "Page",
    ["Submit report", "View cases", "SPARQL dashboard"],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.write(f"**Current role:** {role}")
st.sidebar.write(f"**Language:** {language}")

# ---------------------------------------------------------
# TRANSLATION HELPERS
# ---------------------------------------------------------
def tr(key: str, default_en: str) -> str:
    """
    Translation helper for bilingual labels.
    Uses LABELS from schema.py. If Amharic is selected and we
    have an Amharic translation, returns 'EN / AM'. Otherwise EN.
    """
    if language.startswith("Amharic"):
        if key in LABELS and "am" in LABELS[key]:
            return f"{LABELS[key]['en']} / {LABELS[key]['am']}"
        return default_en
    else:
        if key in LABELS and "en" in LABELS[key]:
            return LABELS[key]["en"]
        return default_en


def section_header(title_en: str, title_am: str = ""):
    """Section header that can show Amharic and English together."""
    if language.startswith("Amharic") and title_am:
        st.subheader(f"{title_en} / {title_am}")
    else:
        st.subheader(title_en)


# ---------------------------------------------------------
# PAGE 1: SUBMIT REPORT
# ---------------------------------------------------------
if page == "Submit report":
    st.title("Incident / Event Reporting Form")
   # st.caption("Prototype based on FieldLab1 data schema – data clerk input screen.")

    with st.form("event_report_form"):
        # 1. Reporting Information
        section_header("1. Reporting Information", "የሪፖርት መረጃ")

        col_r1, col_r2, col_r3 = st.columns(3)

        with col_r1:
            organisation_id = st.number_input(
                tr("organisation_id", "Organisation ID"),
                min_value=0,
                step=1,
                help="Internal code of the organisation collecting this report.",
            )
        with col_r2:
            input_by = st.text_input(
                tr("input_by", "Input by (user name / ID)"),
                help="Person or account entering this data.",
            )
        with col_r3:
            date_recorded = st.date_input(
                tr("date_recorded", "Date report recorded"),
                value=date.today(),
            )

        # 2. Camp / Location
        section_header("2. Camp / Location Information", "የካምፕ መረጃ")

        all_countries = sorted({loc["country"] for loc in LOCATION_REGISTRY})
        selected_country = st.selectbox(
            tr("country", "Country"),
            options=all_countries,
        )

        regions_for_country = sorted(
            {loc["region"] for loc in LOCATION_REGISTRY if loc["country"] == selected_country}
        )
        selected_region = st.selectbox(
            tr("region", "Region / State"),
            options=regions_for_country,
        )

        camps_for_region = sorted(
            {
                loc["camp"]
                for loc in LOCATION_REGISTRY
                if loc["country"] == selected_country and loc["region"] == selected_region
            }
        )
        camp_options = camps_for_region + ["Other (specify)"]
        selected_camp = st.selectbox(
            tr("camp", "Camp / Town"),
            options=camp_options,
        )

        camp_other = ""
        if selected_camp == "Other (specify)":
            camp_other = st.text_input(
                tr("camp_other", "If other, please specify camp / town name")
            )

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            camp_lat = st.number_input(
                tr("latitude", "Latitude (optional)"),
                value=0.0,
                format="%.6f",
            )
        with col_c2:
            camp_lon = st.number_input(
                tr("longitude", "Longitude (optional)"),
                value=0.0,
                format="%.6f",
            )

        # 3. Event Information
        section_header("3. Event Information", "የክስተት መረጃ")

        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            event_date = st.date_input(
                tr("event_date", "Date of event"),
                value=date.today(),
            )
        with col_e2:
            time_range = st.text_input(
                tr("time_range", "Time range (e.g. 10:00–12:00)")
            )
        with col_e3:
            event_location_detail = st.text_input(
                tr("event_location_detail", "Specific place (neighbourhood / site)"),
                help="More detailed description of where in the camp or town.",
            )

        col_e4, col_e5 = st.columns(2)
        with col_e4:
            event_type = st.selectbox(
                tr("event_type", "Type of event"),
                EVENT_TYPES,
            )
        with col_e5:
            event_subtype = st.text_input(
                tr("event_subtype", "Subtype (optional)"),
                help="More specific description, e.g. shelling, looting, GBV, checkpoint violence, etc.",
            )

        # 4. Affected Population
        section_header("4. Affected Population", "ተጎዳዮች")

        col_a1, col_a2 = st.columns(2)
        with col_a1:
            affected_status = st.selectbox(
                tr("affected_status", "Status of affected group"),
                AFFECTED_STATUSES,
            )
        with col_a2:
            affected_number = st.number_input(
                tr("affected_number", "Estimated number affected"),
                min_value=0,
                step=1,
            )

        # 5. Impact / Description
        section_header("5. Impact / Description", "ተፅእኖና መግለጫ")

        impact_description = st.text_area(
            tr("impact_description", "Impact description"),
            height=150,
            help="Describe what happened, who was affected, and how.",
        )

        # 6. Sensitivity Flags
        section_header("6. Sensitivity", "የግላዊነት ደረጃ")

        col_flags1, col_flags2 = st.columns(2)
        with col_flags1:
            is_sensitive = st.checkbox(
                tr("is_sensitive", "Mark as sensitive protection case"),
                help="Restrict detailed access to authorised protection staff.",
            )
        with col_flags2:
            is_anonymous = st.checkbox(
                tr("is_anonymous", "Anonymous report (no personal identifiers)"),
                help="Do not store names or direct identifiers.",
            )

        submitted = st.form_submit_button("Submit report")

    # Handle submission
    if submitted:
        camp_final = selected_camp if selected_camp != "Other (specify)" else camp_other
        sensitive_flag = 1 if is_sensitive else 0
        anonymous_flag = 1 if is_anonymous else 0

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO cases (
                role,
                organisation_id,
                input_by,
                date_recorded,
                country,
                region,
                camp,
                latitude,
                longitude,
                event_date,
                time_range,
                event_location_detail,
                event_type,
                event_subtype,
                affected_status,
                affected_number,
                impact_description,
                is_sensitive,
                is_anonymous,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                role,
                int(organisation_id),
                input_by,
                str(date_recorded),
                selected_country,
                selected_region,
                camp_final,
                float(camp_lat),
                float(camp_lon),
                str(event_date),
                time_range,
                event_location_detail,
                event_type,
                event_subtype,
                affected_status,
                int(affected_number),
                impact_description,
                sensitive_flag,
                anonymous_flag,
                datetime.utcnow().isoformat(),
            ),
        )
        conn.commit()
        conn.close()

        st.success("Report saved successfully to local database (fieldlab1.db).")


# ---------------------------------------------------------
# PAGE 2: VIEW CASES
# ---------------------------------------------------------
if page == "View cases":
    st.title("View reported cases")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT
            id,
            created_at,
            role,
            country,
            region,
            camp,
            event_date,
            event_type,
            affected_status,
            affected_number,
            is_sensitive,
            is_anonymous
        FROM cases
        ORDER BY datetime(created_at) DESC
        """
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        st.info("No cases saved yet. Submit a report first on the 'Submit report' page.")
    else:
        # Build DataFrame
        df = pd.DataFrame(
            rows,
            columns=[
                "ID",
                "Created at",
                "Role",
                "Country",
                "Region",
                "Camp",
                "Event date",
                "Event type",
                "Affected status",
                "Affected number",
                "Sensitive",
                "Anonymous",
            ],
        )

        # Map 0/1 -> Yes/No for readability
        df["Sensitive"] = df["Sensitive"].map({0: "No", 1: "Yes"})
        df["Anonymous"] = df["Anonymous"].map({0: "No", 1: "Yes"})

        st.markdown(f"Total cases in database: **{len(df)}**")

        # -------------------------------
        # SIMPLE FILTERS
        # -------------------------------
        col_f1, col_f2, col_f3 = st.columns(3)

        with col_f1:
            countries = ["All"] + sorted(df["Country"].dropna().unique().tolist())
            selected_country_filter = st.selectbox("Filter by country", countries, index=0)

        with col_f2:
            event_types = ["All"] + sorted(df["Event type"].dropna().unique().tolist())
            selected_event_type_filter = st.selectbox("Filter by event type", event_types, index=0)

        with col_f3:
            hide_sensitive = st.checkbox(
                "Hide sensitive cases",
                value=False,
                help="If checked, rows marked as Sensitive = Yes will be hidden.",
            )

        # Apply filters
        filtered_df = df.copy()

        if selected_country_filter != "All":
            filtered_df = filtered_df[filtered_df["Country"] == selected_country_filter]

        if selected_event_type_filter != "All":
            filtered_df = filtered_df[filtered_df["Event type"] == selected_event_type_filter]

        # -------------------------------
        # ROLE-BASED ACCESS CONTROL (RBAC)
        # -------------------------------
        if role == "Field Worker":
            # Field Workers never see sensitive rows at all
            filtered_df = filtered_df[filtered_df["Sensitive"] == "No"]
            st.info("Sensitive cases are hidden for Field Workers (Do No Harm).")
        else:
            # Sector Officer / Admin can choose to hide sensitive
            if hide_sensitive:
                filtered_df = filtered_df[filtered_df["Sensitive"] == "No"]

        st.markdown(f"Showing **{len(filtered_df)}** case(s) after filters and access rules.")
        st.dataframe(filtered_df, use_container_width=True)

        # ---------------------------------------------------------
        # CASE DETAIL VIEW
        # ---------------------------------------------------------
        if not filtered_df.empty:
            st.markdown("### Case details")

            selected_case_id = st.selectbox(
                "Select a case ID to view full details",
                options=filtered_df["ID"].tolist(),
            )

            if selected_case_id is not None:
                conn = get_connection()
                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT
                        id,
                        role,
                        organisation_id,
                        input_by,
                        date_recorded,
                        country,
                        region,
                        camp,
                        latitude,
                        longitude,
                        event_date,
                        time_range,
                        event_location_detail,
                        event_type,
                        event_subtype,
                        affected_status,
                        affected_number,
                        impact_description,
                        is_sensitive,
                        is_anonymous,
                        created_at
                    FROM cases
                    WHERE id = ?
                    """,
                    (int(selected_case_id),),
                )
                detail_row = cur.fetchone()
                conn.close()

                if detail_row:
                    (
                        d_id,
                        d_role,
                        d_org_id,
                        d_input_by,
                        d_date_recorded,
                        d_country,
                        d_region,
                        d_camp,
                        d_lat,
                        d_lon,
                        d_event_date,
                        d_time_range,
                        d_event_loc_detail,
                        d_event_type,
                        d_event_subtype,
                        d_aff_status,
                        d_aff_number,
                        d_impact_desc,
                        d_is_sensitive,
                        d_is_anonymous,
                        d_created_at,
                    ) = detail_row

                    sens_label = "Yes" if d_is_sensitive else "No"
                    anon_label = "Yes" if d_is_anonymous else "No"

                    st.markdown(
                        f"**Case ID:** {d_id}  |  **Created at:** {d_created_at}  |  "
                        f"**Role (who reported):** {d_role}"
                    )

                    col_d1, col_d2, col_d3 = st.columns(3)
                    with col_d1:
                        st.markdown("**Reporting**")
                        st.write(f"Organisation ID: {d_org_id}")
                        st.write(f"Input by: {d_input_by}")
                        st.write(f"Date recorded: {d_date_recorded}")
                    with col_d2:
                        st.markdown("**Location**")
                        st.write(f"Country: {d_country}")
                        st.write(f"Region: {d_region}")
                        st.write(f"Camp/Town: {d_camp}")
                        st.write(f"Latitude: {d_lat}")
                        st.write(f"Longitude: {d_lon}")
                    with col_d3:
                        st.markdown("**Sensitivity**")
                        st.write(f"Sensitive case: {sens_label}")
                        st.write(f"Anonymous report: {anon_label}")

                    col_d4, col_d5 = st.columns(2)
                    with col_d4:
                        st.markdown("**Event**")
                        st.write(f"Event date: {d_event_date}")
                        st.write(f"Time range: {d_time_range}")
                        st.write(f"Place detail: {d_event_loc_detail}")
                        st.write(f"Event type: {d_event_type}")
                        st.write(f"Subtype: {d_event_subtype}")
                    with col_d5:
                        st.markdown("**Affected population**")
                        st.write(f"Status: {d_aff_status}")
                        st.write(f"Estimated number: {d_aff_number}")

                    st.markdown("**Impact description**")
                    st.write(d_impact_desc if d_impact_desc else "No description provided.")

        # ---------------------------------------------------------
        # EXPORT & UPLOAD (CSV + RDF Turtle)
        # ---------------------------------------------------------
        st.markdown("### Export / upload filtered cases")

        # Export rules:
        # - Admin: export all filtered_df
        # - Others: export only non-sensitive
        if role == "Admin":
            export_df = filtered_df.copy()
            st.caption("Admin: exporting all filtered cases (including sensitive).")
        else:
            export_df = filtered_df[filtered_df["Sensitive"] == "No"].copy()
            st.caption("Non-admin: exporting only non-sensitive cases.")

        if export_df.empty:
            st.warning("No cases available to export with the current filters and role.")
        else:
            # Prepare CSV
            csv_data = export_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="fieldlab_cases_filtered.csv",
                mime="text/csv",
            )

            # Prepare RDF (Turtle)
            rdf_data = dataframe_to_rdf(export_df)
            st.download_button(
                label="Download RDF (Turtle)",
                data=rdf_data,
                file_name="fieldlab_cases_filtered.ttl",
                mime="text/turtle",
            )

            # Admin-only: upload to triple store
            if role == "Admin":
                st.markdown("#### Triple store upload (Admin only)")
                if st.button("Upload RDF to AllegroGraph"):
                    success, msg, repo_url = upload_to_allegrograph(rdf_data)
                    if success:
                        st.success(msg)
                        if repo_url:
                            st.write("Repository URL (share with FieldLab 7 / for FDP):")
                            st.code(repo_url)
                    else:
                        st.error(msg)


# ---------------------------------------------------------
# PAGE 3: SPARQL DASHBOARD (READ FROM ALLEGROGRAPH)
# ---------------------------------------------------------
if page == "SPARQL dashboard":
    st.title("SPARQL dashboard – AllegroGraph")

    st.caption(
        "This page runs live SPARQL queries against the AllegroGraph "
        "repository using the same credentials as the ETL layer."
    )

    # Example queries
    sample_queries = {
        "All incidents (limit 20)": """
PREFIX cd: <https://fieldlab1.example.org/cdm/>

SELECT ?incident ?eventDate ?eventType ?region ?camp ?affectedNumber
WHERE {
  ?incident a cd:Incident .
  OPTIONAL { ?incident cd:eventDate ?eventDate . }
  OPTIONAL { ?incident cd:eventType ?eventType . }
  OPTIONAL { ?incident cd:region ?region . }
  OPTIONAL { ?incident cd:camp ?camp . }
  OPTIONAL { ?incident cd:affectedNumber ?affectedNumber . }
}
LIMIT 20
""",
        "Incidents by region": """
PREFIX cd: <https://fieldlab1.example.org/cdm/>

SELECT ?region (COUNT(?incident) AS ?count)
WHERE {
  ?incident a cd:Incident ;
            cd:region ?region .
}
GROUP BY ?region
ORDER BY DESC(?count)
""",
        "Incidents by event type": """
PREFIX cd: <https://fieldlab1.example.org/cdm/>

SELECT ?eventType (COUNT(?incident) AS ?count)
WHERE {
  ?incident a cd:Incident ;
            cd:eventType ?eventType .
}
GROUP BY ?eventType
ORDER BY DESC(?count)
""",
    }

    query_name = st.selectbox(
        "Choose a predefined query",
        list(sample_queries.keys()),
    )

    query_text = sample_queries[query_name]
    st.markdown("#### SPARQL query")
    st.code(query_text.strip(), language="sparql")

    st.markdown("You can also edit the query before running:")
    editable_query = st.text_area(
        "Edit query",
        value=query_text.strip(),
        height=220,
    )

    if st.button("Run SPARQL query"):
        try:
            resp = requests.get(
                SPARQL_ENDPOINT,
                params={"query": editable_query},
                auth=(AG_USERNAME, AG_PASSWORD),
                headers={"Accept": "application/sparql-results+json"},
                timeout=30,
            )
        except Exception as e:
            st.error(f"Request error: {e}")
        else:
            if resp.status_code != 200:
                st.error(f"SPARQL request failed (HTTP {resp.status_code}):\n{resp.text[:500]}")
            else:
                data = resp.json()
                rows = data.get("results", {}).get("bindings", [])
                if not rows:
                    st.info("Query returned no results.")
                else:
                    cols = list(rows[0].keys())
                    records = []
                    for r in rows:
                        records.append({c: r[c]["value"] if c in r else None for c in cols})
                    results_df = pd.DataFrame(records)
                    st.markdown("#### Results")
                    st.dataframe(results_df, use_container_width=True)
