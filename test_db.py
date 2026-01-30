import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "eggs"))

from sqlmodel import create_engine, Session, SQLModel
from eggs.db import ListModel, ItemModel, init_db


# Test creating tables with updated models
def test_table_creation():
    # Create an in-memory database
    engine = create_engine("sqlite:///:memory:")

    # Initialize database with updated models
    init_db(engine)

    # Check if tables were created properly
    with Session(engine) as session:
        # Test creating a list
        list_model = ListModel(name="test_list")
        session.add(list_model)
        session.commit()
        session.refresh(list_model)

        # Test creating an item
        item_model = ItemModel(name="test_item", list_id=list_model.id)
        session.add(item_model)
        session.commit()
        session.refresh(item_model)

        # Test reading them back
        lists = session.exec(SQLModel.select(ListModel)).all()
        items = session.exec(SQLModel.select(ItemModel)).all()

        print(f"Created {len(lists)} lists and {len(items)} items")
        assert len(lists) == 1
        assert len(items) == 1
        print("All tests passed!")


if __name__ == "__main__":
    test_table_creation()
