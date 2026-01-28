import pytest

from eggs.api import app
from fastapi.testclient import TestClient

from eggs.db import get_db
from tests.db import db_session


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def test_read_lists_empty(client):
    """Test reading lists when database is empty"""
    response = client.get("/api/v1/lists/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_list_success(client):
    """Test creating a new list successfully"""
    response = client.post("/api/v1/lists/todo")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "todo"}


def test_read_lists_after_creation(client):
    """Test reading lists after creating a new list"""
    # Create a list first
    client.post("/api/v1/lists/todo")
    # Read all lists
    response = client.get("/api/v1/lists/")
    assert response.status_code == 200
    assert response.json() == ["todo"]


def test_create_duplicate_list(client):
    """Test creating a duplicate list fails appropriately"""
    # Create a list
    client.post("/api/v1/lists/todo")
    # Try to create the same list again
    response = client.post("/api/v1/lists/todo")
    assert response.status_code == 400
    assert "already exists" in response.json().get("detail", "")


def test_delete_list_success(client):
    """Test deleting a list successfully"""
    # Create a list first
    client.post("/api/v1/lists/todo")
    # Delete the list
    response = client.delete("/api/v1/lists/todo")
    assert response.status_code == 200
    assert response.json() == {"message": "List 'todo' deleted successfully"}


def test_delete_nonexistent_list(client):
    """Test deleting a list that doesn't exist"""
    # Try to delete a non-existent list
    response = client.delete("/api/v1/lists/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "List not found"}


def test_create_item_success(client):
    """Test creating an item in a list successfully"""
    # Create a list first
    client.post("/api/v1/lists/shopping")
    # Create an item
    response = client.post("/api/v1/lists/shopping/items/", json={"name": "milk"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "list_id": 1, "name": "milk"}


def test_create_duplicate_item(client):
    """Test creating a duplicate item in the same list fails"""
    # Create a list and item
    client.post("/api/v1/lists/shopping")
    client.post("/api/v1/lists/shopping/items/", json={"name": "milk"})
    # Try to create the same item again
    response = client.post("/api/v1/lists/shopping/items/", json={"name": "milk"})
    assert response.status_code == 400
    assert "already exists" in response.json().get("detail", "")


def test_create_item_nonexistent_list(client):
    """Test creating an item in a non-existent list fails"""
    response = client.post("/api/v1/lists/nonexistent/items/", json={"name": "milk"})
    assert response.status_code == 404
    assert response.json() == {"detail": "List not found"}


def test_read_items_empty_list(client):
    """Test reading items from an empty list"""
    # Create a list
    client.post("/api/v1/lists/shopping")
    # Read items
    response = client.get("/api/v1/lists/shopping/items/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_items_after_creation(client):
    """Test reading items after creating them"""
    # Create a list and items
    client.post("/api/v1/lists/shopping")
    client.post("/api/v1/lists/shopping/items/", json={"name": "milk"})
    client.post("/api/v1/lists/shopping/items/", json={"name": "eggs"})
    # Read items
    response = client.get("/api/v1/lists/shopping/items/")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 2
    assert "milk" in items
    assert "eggs" in items


def test_read_items_nonexistent_list(client):
    """Test reading items from a non-existent list fails"""
    response = client.get("/api/v1/lists/nonexistent/items/")
    assert response.status_code == 404
    assert response.json() == {"detail": "List not found"}


def test_delete_item_success(client):
    """Test deleting an item successfully"""
    # Create a list and item
    client.post("/api/v1/lists/shopping")
    client.post("/api/v1/lists/shopping/items/", json={"name": "milk"})
    # Delete the item
    response = client.delete("/api/v1/lists/shopping/items/milk")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Item 'milk' deleted successfully from list 'shopping'"
    }


def test_delete_nonexistent_item(client):
    """Test deleting a non-existent item fails"""
    # Create a list
    client.post("/api/v1/lists/shopping")
    # Try to delete a non-existent item
    response = client.delete("/api/v1/lists/shopping/items/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_same_item_different_lists(client):
    """Test that the same item name can exist in different lists"""
    # Create two lists
    client.post("/api/v1/lists/shopping")
    client.post("/api/v1/lists/todo")
    # Create the same item in both lists
    response1 = client.post("/api/v1/lists/shopping/items/", json={"name": "milk"})
    response2 = client.post("/api/v1/lists/todo/items/", json={"name": "milk"})
    assert response1.status_code == 200
    assert response2.status_code == 200
    # Verify items are in both lists
    shopping_items = client.get("/api/v1/lists/shopping/items/").json()
    todo_items = client.get("/api/v1/lists/todo/items/").json()
    assert "milk" in shopping_items
    assert "milk" in todo_items


def test_cascade_delete_items(client):
    """Test that deleting a list cascades to delete its items"""
    # Create a list with items
    client.post("/api/v1/lists/shopping")
    client.post("/api/v1/lists/shopping/items/", json={"name": "milk"})
    client.post("/api/v1/lists/shopping/items/", json={"name": "eggs"})
    # Verify items exist
    items_before = client.get("/api/v1/lists/shopping/items/").json()
    assert len(items_before) == 2
    # Delete the list
    client.delete("/api/v1/lists/shopping")
    # Try to read items from the deleted list (should fail)
    response = client.get("/api/v1/lists/shopping/items/")
    assert response.status_code == 404
    assert response.json() == {"detail": "List not found"}
