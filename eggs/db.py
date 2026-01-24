from sqlmodel import create_engine, Session, SQLModel, Field
from typing import Generator

DATABASE_URL = "sqlite:///lists.db"
engine = create_engine(DATABASE_URL, echo=True)


class ListModel(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str


def init_db():
    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
