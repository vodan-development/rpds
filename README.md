# Secure FAIR Refugee Protection Information System (RPDS)
## 1. Project Overview

This repository contains the FAIR-aligned application designed for the structured collection, management, and semantic publication of refugee protection information. Developed by the **Aksum University Group** (Zinabu Haile, Haftom Mekonnen), this system bridges the gap between grassroots field reporting and high-level semantic interoperability.

## 2. Core Objectives

   - ✅ **Secure Reporting**: Provide a user-friendly, multilingual interface for field workers to report sensitive incidents.
   - ✅ **FAIR Implementation**: Transform raw data into RDF triples using a Common Data Model (CDM).
   - ✅ **Semantic Integration**: Store and query data via AllegroGraph using SPARQL endpoints.
   - ✅ **Access Control**: Implement role-based viewing (Admin, Sector Officer, Field Worker) to manage data sensitivity.

## 3. System Architecture
The application follows a modular architecture:
   - ✅ **Frontend (Streamlit)**: Streamlit-based UI for data entry and SPARQL querying.A supporting multilingual UI  English, Amharic, and Tigrigna.
   - ✅ **Storage (SQLite)**: Local database (fieldlab1.db) for temporary data persistence before RDF transformation.  
   - ✅ **ETL Pipeline (rdflib)**: Converts SQLite records into RDF (Turtle format) using standardized namespaces (FAIR, GEO, CDM).
   - ✅ **Triple Store (AllegroGraph)**: Semantic storage and SPARQL endpoint for federated data access.

## 4. Technical Specifications
  ## Data Schema (`# schema.py`)
      The system utilizes a controlled vocabulary for:
   - **Event Types**: Armed conflict, Violence against civilians, Political Decision, Forced displacement, etc.
   - **Location Registry**: Pre-defined camps across Ethiopia (Tigray, Amhara), Sudan, Uganda, and Kenya.
   - **Multilingual Labels**: All UI elements and data categories are mapped in English (en), Amharic (am), and Tigrigna (ti).

 ## Database & ETL (`# db.py, etl.py`)

  - **SQLite Schema**: Tracks 33 fields including incident coordinates, perpetrator descriptions, and sensitivity flags.
   - **RDF Mapping**: Uses BASE, CDM, and GEO namespaces to ensure data is Findable and Interoperable.

## 5. Installation & Setup
   Prerequisites
     Ensure you have Python and Anaconda installed. You will need the following libraries:
   
   Install Anaconda
   
    Anaconda 26+
   
   *Go to* 
   <https://www.anaconda.com/download>

   Install Python
    
     Python 3.13+
   *Go to* 
   <https://www.python.org/downloads/>
  
  
```markdown
     pip install streamlit rdflib requests pandas numpy plotly
     pip install PyYAML agraph-python
```
  **Running the Application**

  **1. Clone the Repository**:
```markdown
     git clone https://github.com/VODAN-Development/RPDS
```
  or
    *GitHub Link to clone* 
    <https://github.com/VODAN-Development/RPDS>

 **2. Initialize the System:**

  **Run the app via Streamlit:**

```markdown
     python -m streamlit run “C:\Users\<your-pc-user>\Documents\<downloaded-app>\RPDS-main\RPDS-main\app.py"
     
- ✅ Replace <your-pc-user> with your PCs user
- ✅ Replace <downloaded-app> with the name of the folder which you’ve downloaded the app to
- ✅ REPLACE the text between “  is installed on your computer (you can find this by clicking properties, and then you just need to copy-paste and add \app.py at the end OR dragging the file to Anaconda and it will autofill the pathway).

```

### Access Credentials

| Role	| Username	| Password |
|---------|-------------|-------------|
| **Admin** | admin | admin123|
| **Sector Officer** |officer	|officer123 |
| **Field Worker** |fieldworker	| worker123 | 

## 6. FAIR Principles Alignment
   - ✅ **Findable**: Data is indexed and discoverable via a dedicated SPARQL endpoint.
   - ✅ **Accessible**: Protected by role-based access control (RBAC) and stored in AllegroGraph Cloud.
   - ✅ **Interoperable**: Uses RDF Turtle serialization and standardized vocabularies (DC TERMS, PROV, GEO).
   - ✅ **Reusable**: Documented metadata schemas and "Do No Harm" ethical data handling ensure safe long-term reuse.

## 7 Repository Structure

  - ✅ **app.py**: The main entry point; handles the multilingual UI and role-based logic.
  - ✅ **db.py**: Manages the SQLite connection and local record initialization.
  - ✅ **etl.py**: Logic for converting relational records into RDF triples and uploading to AllegroGraph.
 - ✅ **schema.py**: Contains the controlled vocabularies (Event Types, Locations) and multilingual translation mappings.
 - ✅ **Presentation.pptx**: Documentation regarding project objectives and system walkthroughs.
## 8 User Interface Features

 - ✅ **Multilingual Support**: Fully accessible in English, Amharic, and Tigrigna.
 - ✅ **Role-Based Access Control (RBAC)**: Distinct interfaces for Admin, Sector Officer, and Field Worker.
 - ✅ **Geospatial Reporting**: Integrated mapping for incident locations using WGS84 coordinates.

## 9. Collaboration

This project is part of the VODAN 2026 FAIR System Engineering Training.

## 10. License

This repository is intended for educational and research purposes under VODAN AFRICA 2026.
