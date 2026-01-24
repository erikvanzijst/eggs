from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import Session
import pytest

from eggs.db import init_db


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    init_db(engine)
    with Session(engine) as session:
        yield session
