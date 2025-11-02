import sqlite3
import pandas as pd
from datetime import datetime
import os

# Maak map voor database
DB_NAME = "data/bookings.db"
os.makedirs("data", exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Tabel voor boekingen
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            service TEXT,
            employee TEXT,
            date TEXT,
            time TEXT,
            status TEXT DEFAULT 'bevestigd',
            created_at TEXT
        )
    ''')
    
    # Tabel voor medewerkers
    c.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
    ''')
    
    # Voeg standaard medewerkers toe
    employees = ["Anna", "Lisa", "Tom"]
    for emp in employees:
        c.execute("INSERT OR IGNORE INTO employees (name) VALUES (?)", (emp,))
    
    conn.commit()
    conn.close()

def get_employees():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT name FROM employees", conn)
    conn.close()
    return df['name'].tolist() if not df.empty else []

def add_booking(name, phone, service, employee, date, time):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    created_at = datetime.now().isoformat()
    c.execute("""
        INSERT INTO bookings (name, phone, service, employee, date, time, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, phone, service, employee, date, time, created_at))
    conn.commit()
    booking_id = c.lastrowid
    conn.close()
    return booking_id

def get_bookings():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM bookings ORDER BY date DESC, time DESC", conn)
    conn.close()
    return df

def get_available_slots(date, duration=30):
    import pandas as pd
    from datetime import timedelta
    start = pd.Timestamp(f"{date} 09:00")
    end = pd.Timestamp(f"{date} 18:00")
    slots = []
    current = start
    while current < end:
        slot_time = current.strftime("%H:%M")
        slots.append(slot_time)
        current += timedelta(minutes=duration)
    return slots
