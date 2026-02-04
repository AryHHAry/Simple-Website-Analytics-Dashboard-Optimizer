import sqlite3
import pandas as pd
import os

DB_PATH = "analytics_data.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table for visits (anonymized)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            visitor_id TEXT,
            page TEXT,
            source TEXT,
            country TEXT,
            duration INTEGER
        )
    ''')
    
    # Table for alerts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            alert_type TEXT,
            message TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def log_visit(visitor_id, page, source, country, duration):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO visits (visitor_id, page, source, country, duration)
        VALUES (?, ?, ?, ?, ?)
    ''', (visitor_id, page, source, country, duration))
    conn.commit()
    conn.close()

def get_visit_data():
    if not os.path.exists(DB_PATH):
        init_db()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM visits", conn)
    conn.close()
    return df

def clear_data():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()
