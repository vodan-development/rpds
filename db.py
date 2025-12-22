"""
db.py – SQLite helper functions for FieldLab1 prototype.
This keeps all database-related code separate from the UI.
"""

from pathlib import Path
import sqlite3

# Path to the SQLite database file
DB_PATH = Path("fieldlab1.db")


def get_connection():
    """
    Open a connection to the SQLite database.
    Each call returns a new connection; the caller must close it.
    """
    return sqlite3.connect(DB_PATH)


def init_db():
    """
    Create the 'cases' table if it does not exist.
    The schema here matches the fields we collect in the form.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            organisation_id INTEGER,
            input_by TEXT,
            date_recorded TEXT,
            country TEXT,
            region TEXT,
            camp TEXT,
            latitude REAL,
            longitude REAL,
            event_date TEXT,
            time_range TEXT,
            event_location_detail TEXT,
            event_type TEXT,
            event_subtype TEXT,
            affected_status TEXT,
            affected_number INTEGER,
            impact_description TEXT,
            is_sensitive INTEGER,
            is_anonymous INTEGER,
            created_at TEXT
        );
        """
    )
    conn.commit()
    conn.close()
