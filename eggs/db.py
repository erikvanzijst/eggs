import sqlite3

DATABASE_URL = "lists.db"

def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS lists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()


def get_db():
    conn = sqlite3.connect(DATABASE_URL)
    init_db(conn)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
