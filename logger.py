# logger.py
import sqlite3
from datetime import datetime

DB_PATH = "runs_log.db"

def init_db():
    """Create table if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            script_name TEXT,
            timestamp TEXT,
            status TEXT,
            records_processed INTEGER,
            error_message TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_run(script_name, status, records_processed=0, error_message=None):
    """Insert a new log entry"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO runs (script_name, timestamp, status, records_processed, error_message)
        VALUES (?, ?, ?, ?, ?)
    """, (
        script_name,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        status,
        records_processed,
        error_message
    ))
    conn.commit()
    conn.close()