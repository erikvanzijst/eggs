#!/usr/bin/env python3

"""Simple test to verify database operations work with renamed tables"""

from sqlalchemy import create_engine
from sqlmodel import Session
from eggs.db import init_db, ListModel, ItemModel


def test_database_operations():
    # Create in-memory database
    engine = create_engine("sqlite:///:memory:", echo=True)

    # Initialize database with our models
    init_db(engine)

    # Test creating a list
    with Session(engine) as session:
        # Create a list
        list_model = ListModel(name="Test List")
        session.add(list_model)
        session.commit()
        session.refresh(list_model)

        # Create an item
        item_model = ItemModel(name="Test Item", list_id=list_model.id)
        session.add(item_model)
        session.commit()
        session.refresh(item_model)

        # Verify the data was saved
        lists = session.query(ListModel).all()
        items = session.query(ItemModel).all()

        print(f"Created {len(lists)} lists and {len(items)} items")
        print(f"List name: {lists[0].name}")
        print(f"Item name: {items[0].name}")
        print("Database operations test passed!")


if __name__ == "__main__":
    test_database_operations()
