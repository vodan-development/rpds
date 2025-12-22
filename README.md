FieldLab1 – Secure FAIR Refugee Protection Information System
1. Project Overview

This repository contains the final implementation of FieldLab1, a secure and FAIR-aligned application designed to support the structured collection, management, and semantic publication of refugee protection information in humanitarian contexts.

The project addresses challenges related to:

Sensitive data handling

Multilingual data collection

Role-based access control

FAIR data publication

Interoperability with a federated data space

The system was developed as part of the Data Science in Practice course at Leiden University.

2. Problem Context

Humanitarian field workers often operate in low-resource environments where:

Connectivity is limited

Users have varying technical skills

Data sensitivity is critical

Refugee safety must be protected (“Do No Harm” principle)

This project provides a user-friendly interface for data clerks and protection officers while ensuring that collected data can be securely transformed into RDF and published to a FAIR Data Point (FDP) via a semantic triple store.

3. System Architecture

The application follows a modular architecture:

User Interface (UI)
Built with Streamlit, supporting multilingual labels and role-based access.

Local Storage
Data is temporarily stored in a local SQLite database.

ETL Pipeline
Structured records are transformed into RDF (Turtle) using rdflib.

Semantic Storage
RDF data is uploaded to AllegroGraph Cloud.

Query Layer
Data is exposed via a SPARQL endpoint for integration with other FieldLabs and the FDP.

4. Technologies Used

Python 3

Streamlit

SQLite

Pandas

rdflib

AllegroGraph Cloud

SPARQL

HTTP / REST APIs

5. Repository Structure
   fieldlab1/
│
├── app.py              # Streamlit user interface
├── db.py               # SQLite database helpers
├── schema.py           # Controlled vocabularies & CDM labels
├── etl.py              # RDF generation & AllegroGraph upload
├── requirements.txt    # Python dependencies
│
├── 
   FieldLab1_Final_Presentation.pptx
│
└── README.md

6. Running the Application
Prerequisites

Python 3.9+

pip

Installation
pip install -r requirements.txt

Run the applicationstreamlit run app.py

streamlit run app.py
and this UI will open in browser.

7. User Interface Features

Structured form-based data input

Hierarchical location selection

Controlled vocabularies

Multilingual labels (English + Amharic-ready)

Role-based access control:

Field Worker

Sector Officer

Admin

Case review and filtering dashboard

Export to CSV and RDF (Turtle)

8. ETL & Semantic Integration

The ETL process performs the following steps:

Read structured records from SQLite

Transform records into RDF using a Community Data Model (CDM)

Serialize RDF as Turtle (.ttl)

Upload data to AllegroGraph Cloud

Expose data through a SPARQL endpoint

This ensures interoperability, traceability, and reuse of the data.

9. FAIR & FDP Integration

The dataset complies with FAIR principles:

Findable: Published via a SPARQL endpoint

Accessible: Role-based access rules enforced

Interoperable: RDF + shared vocabularies

Reusable: Documented schema and semantics

The AllegroGraph repository URL and SPARQL endpoint are shared with FieldLab 7 for FDP integration.

10. Security, Ethics & Legal Compliance

GDPR-aware data handling

Sensitive data classification

Role-based access control (RBAC)

Anonymous reporting options

Encryption in transit (HTTPS)

Alignment with humanitarian “Do No Harm” principles

No AI systems are deployed, and the AI Act is therefore not applicable.

11. Collaboration & Integration

This project integrates with:

FieldLab 7 (Federated Lighthouse / FDP)

Shared Community Data Models

Cross-FieldLab semantic interoperability

12. License

This repository is intended for educational and research purposes within the Data Science in Practice course.





For reuse see the [license](https://github.com/VODAN-Development/FAIR-Data-Point/blob/main/LICENSE).
For contributing to this project see the [contributor file](https://github.com/VODAN-Development/FAIR-Data-Point/blob/main/CONTRIBUTING.md).
For issue reporting use the [issue board](https://github.com/VODAN-Development/FAIR-Data-Point/issues).
