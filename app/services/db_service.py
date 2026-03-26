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
        roll TEXT UNIQUE
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

def add_student(name, roll):
    conn = get_conn();
    cur = conn.cursor()

    #c check if roll already exists
    cur.execute("SELECT id FROM students WHERE roll = ?", 
                (roll, ))
    row = cur.fetchone();

    if row:
        conn.close()
        return row[0] # already exists -> return existing id
    
    cur.execute(
        "INSERT INTO students (name, roll) VALUES (?, ?)",
        (name, roll)
    )

    student_id = cur.lastrowid
    conn.commit()
    conn.close()

    return student_id

# embeddings are stored in raw bytes
# to restore we gotta specify that it is flaot32
def add_embedding(student_id, embedding):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO embeddings (student_id, embedding) VALUES (?, ?)",
        (student_id, embedding.tobytes())
    )

    conn.commit()
    conn.close()

def load_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    SELECT students.id, students.name, students.roll, embeddings.embedding
    FROM embeddings
    JOIN students ON embeddings.student_id = students.id
    """)

    rows = cur.fetchall()
    conn.close()

    db = {}

    for student_id, name, roll, emb_blob in rows:
        emb = np.frombuffer(emb_blob, dtype=np.float32)

        if student_id not in db:
            db[student_id] = {
                "name": name,
                "roll": roll,
                "embeddings": []
            }

        db[student_id]["embeddings"].append(emb)

    return db