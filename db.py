# db.py – SQLite helper functions for RPDS
# This keeps all database-related code separate from the UI.

from pathlib import Path
import sqlite3

# Path to the SQLite database file
DB_PATH = Path("rpds.db")


def get_connection():
    # Open a connection to the SQLite database.
    # Each call returns a new connection; the caller must close it.
    return sqlite3.connect(DB_PATH)

def init_db():
    # Create the 'cases' table if it does not exist.
    # The schema here matches the fields we collect in the form.
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            organisation_id INTEGER,
            input_by TEXT,
            date_received TEXT,
            date_recorded TEXT,
            camp_name TEXT,
            camp_id INTEGER,
            country TEXT,
            region TEXT,
            town TEXT,
            village_name TEXT,
            latitude REAL,
            longitude REAL,
            event_date TEXT,
            time_range TEXT,
            event_location_detail TEXT,
            event_type TEXT,
            event_subtype TEXT,
            affected_status TEXT,
            affected_number INTEGER,
            ethnicity TEXT,
            affected_target TEXT,            
            impact_description TEXT,
            affiliation TEXT,
            age INTEGER,
            gender TEXT,
            perpetrator_description TEXT,
            involved_category TEXT,
            involvement_description TEXT,
            is_sensitive INTEGER,
            is_anonymous INTEGER,
            created_at TEXT
        );
        """
    )
    conn.commit()
    conn.close()

#----------------------------------------------------------------------------------------#
#--- DELETE Definition Start here -------#
#It works, you can uncomment 
# Please ensure that lines 627–657 in app.py are also uncommented and implemented.
#April 29,2026
#----------------------------------------------------------------------------------------#


# def delete_case(case_id):
#     """Deletes a case record by ID from the SQLite database."""
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute("DELETE FROM cases WHERE id = ?", (case_id,))
#     conn.commit()
#     conn.close()
#--- DELETE Definition end here -------#    