import os
from typing import Generator, Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import create_engine, Session, SQLModel, Field, Relationship

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///lists.db")
engine = create_engine(DATABASE_URL, echo=False)


class ListModel(SQLModel, table=True):
    __tablename__ = "lists"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    items: list["ItemModel"] = Relationship(back_populates="list", cascade_delete=True)


class ItemModel(SQLModel, table=True):
    __tablename__ = "items"
    __table_args__ = (UniqueConstraint("list_id", "name", name="uq_item_list_name"),)

    id: int = Field(default=None, primary_key=True)
    list_id: int = Field(foreign_key="lists.id", ondelete="CASCADE")
    name: str
    list: Optional[ListModel] = Relationship(back_populates="items")


def init_db(engine):
    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
