import sqlite3
import numpy as np

DB_PATH = "access_system.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            embedding BLOB NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS access_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            name TEXT,
            hr REAL,
            spo2 REAL,
            bp TEXT,
            rr REAL,
            verdict TEXT
        )
    """)
    conn.commit()
    conn.close()


def add_user(name, embedding):
    """embedding: numpy array (512,) float32"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO users (name, embedding) VALUES (?, ?)",
        (name, embedding.astype(np.float32).tobytes()),
    )
    conn.commit()
    conn.close()


def get_all_users():
    """Returns list of (name, embedding_ndarray)"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, embedding FROM users")
    rows = c.fetchall()
    conn.close()

    users = []
    for name, emb_blob in rows:
        emb = np.frombuffer(emb_blob, dtype=np.float32)
        users.append((name, emb))
    return users


def log_access(timestamp, name, hr, spo2, bp, rr, verdict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """INSERT INTO access_log (timestamp, name, hr, spo2, bp, rr, verdict)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (timestamp, name, hr, spo2, bp, rr, verdict),
    )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized: access_system.db")