import sqlite3

import pytest

from eggs.db import init_db


@pytest.fixture
def db_session():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    init_db(conn)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()
