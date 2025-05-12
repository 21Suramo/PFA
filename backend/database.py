# backend/database.py

import sqlite3

DB_NAME = "data.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            temperature TEXT,
            pression TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_reading(timestamp, temperature, pression):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO readings (timestamp, temperature, pression) VALUES (?, ?, ?)",
        (timestamp, temperature, pression)
    )
    conn.commit()
    conn.close()

def get_all_readings():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM readings ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [
        {"id": r[0], "timestamp": r[1], "temperature": r[2], "pression": r[3]}
        for r in rows
    ]

def get_latest_reading():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM readings ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "timestamp": row[1], "temperature": row[2], "pression": row[3]}
    return None
