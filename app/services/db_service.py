import sqlite3
import numpy as np

DB_PATH = "data/app.db"


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS embeddings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        embedding BLOB,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    """)

    conn.commit()
    conn.close()