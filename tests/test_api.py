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
    assert response.status_code == 409
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
    response = client.post("/api/v1/lists/shopping/items/milk")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "list_id": 1,
        "name": "milk",
        "is_in_cart": False,
    }


def test_create_duplicate_item(client):
    """Test creating a duplicate item in the same list fails"""
    # Create a list and item
    client.post("/api/v1/lists/shopping")
    client.post("/api/v1/lists/shopping/items/milk")
    # Try to create the same item again
    response = client.post("/api/v1/lists/shopping/items/milk")
    assert response.status_code == 409
    assert "already exists" in response.json().get("detail", "")


def test_create_item_nonexistent_list(client):
    """Test creating an item in a non-existent list fails"""
    response = client.post("/api/v1/lists/nonexistent/items/milk")
    assert response.status_code == 404


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
    client.post("/api/v1/lists/shopping/items/milk")
    client.post("/api/v1/lists/shopping/items/eggs")
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


def test_delete_item_success(client):
    """Test deleting an item successfully"""
    # Create a list and item
    client.post("/api/v1/lists/shopping")
    client.post("/api/v1/lists/shopping/items/milk")
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


def test_same_item_different_lists(client):
    """Test that the same item name can exist in different lists"""
    # Create two lists
    client.post("/api/v1/lists/shopping")
    client.post("/api/v1/lists/todo")
    # Create the same item in both lists
    response1 = client.post("/api/v1/lists/shopping/items/milk")
    response2 = client.post("/api/v1/lists/todo/items/milk")
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
    client.post("/api/v1/lists/shopping/items/milk")
    client.post("/api/v1/lists/shopping/items/eggs")
    # Verify items exist
    items_before = client.get("/api/v1/lists/shopping/items/").json()
    assert len(items_before) == 2
    # Delete the list
    client.delete("/api/v1/lists/shopping")
    # Try to read items from the deleted list (should fail)
    response = client.get("/api/v1/lists/shopping/items/")
    assert response.status_code == 404


def test_create_list_empty_name(client):
    """Test creating a list with an empty name fails"""
    # Test with the correct endpoint, but since we can't pass name as a parameter
    # in the body, the test just verifies that we can't create an empty name
    # in the URL path - which results in 405 error since the endpoint doesn't exist
    response = client.post("/api/v1/lists/")
    assert response.status_code == 405


def test_create_list_long_name(client):
    """Test creating a list with a name exceeding 100 characters fails"""
    long_name = "a" * 101
    response = client.post(f"/api/v1/lists/{long_name}")
    assert response.status_code == 422
    assert "string_too_long" in response.json().get("detail", [{}])[0].get("type")


def test_create_list_invalid_characters(client):
    """Test creating a list with invalid characters fails"""
    response = client.post("/api/v1/lists/list@name")
    assert response.status_code == 422
    # Check that the error message contains the expected pattern
    detail = response.json().get("detail", [])
    assert len(detail) > 0
    assert "pattern" in str(detail[0].get("msg", ""))


def test_create_item_long_name(client):
    """Test creating an item with a name exceeding 100 characters fails"""
    # Create a list first
    client.post("/api/v1/lists/todo")
    long_name = "a" * 101
    response = client.post(f"/api/v1/lists/todo/items/{long_name}")
    assert response.status_code == 422
    # Check that the error message contains the expected max_length error
    detail = response.json().get("detail", [])
    assert len(detail) > 0
    assert "max_length" in str(detail[0].get("ctx", {}))


def test_create_item_invalid_characters(client):
    """Test creating an item with invalid characters fails"""
    # Create a list first
    client.post("/api/v1/lists/todo")
    response = client.post("/api/v1/lists/todo/items/item@name")
    assert response.status_code == 422
    # Check that the error message contains the expected pattern
    detail = response.json().get("detail", [])
    assert len(detail) > 0
    assert "pattern" in str(detail[0].get("msg", ""))


def test_get_item_success(client):
    """Test getting an item by name successfully"""
    # Create a list and item
    client.post("/api/v1/lists/shopping")
    client.post("/api/v1/lists/shopping/items/milk")
    # Get the item
    response = client.get("/api/v1/lists/shopping/items/milk")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "list_id": 1,
        "name": "milk",
        "is_in_cart": False,
    }


def test_get_item_not_found(client):
    """Test getting a non-existent item fails"""
    # Create a list
    client.post("/api/v1/lists/shopping")
    # Try to get a non-existent item
    response = client.get("/api/v1/lists/shopping/items/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_update_item_toggle_flag_false_to_true(client):
    """Test updating an item's is_in_cart flag from False to True"""
    # Create a list and item
    client.post("/api/v1/lists/shopping")
    client.post("/api/v1/lists/shopping/items/milk")

    # Update the item to set is_in_cart=True
    response = client.put(
        "/api/v1/lists/shopping/items/milk", json={"is_in_cart": True}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "list_id": 1,
        "name": "milk",
        "is_in_cart": True,
    }


def test_update_item_toggle_flag_true_to_false(client):
    """Test updating an item's is_in_cart flag from True to False"""
    # Create a list and item
    client.post("/api/v1/lists/shopping")
    client.post("/api/v1/lists/shopping/items/milk")

    # First update to set is_in_cart=True
    response1 = client.put(
        "/api/v1/lists/shopping/items/milk", json={"is_in_cart": True}
    )
    assert response1.status_code == 200

    # Then update to set is_in_cart=False
    response2 = client.put(
        "/api/v1/lists/shopping/items/milk", json={"is_in_cart": False}
    )
    assert response2.status_code == 200
    assert response2.json() == {
        "id": 1,
        "list_id": 1,
        "name": "milk",
        "is_in_cart": False,
    }


def test_update_item_toggle_flag_idempotent(client):
    """Test that toggling the flag multiple times with the same value is idempotent"""
    # Create a list and item
    client.post("/api/v1/lists/shopping")
    client.post("/api/v1/lists/shopping/items/milk")

    # Update multiple times with the same value (should be idempotent)
    response1 = client.put(
        "/api/v1/lists/shopping/items/milk", json={"is_in_cart": True}
    )
    assert response1.status_code == 200
    assert response1.json() == {
        "id": 1,
        "list_id": 1,
        "name": "milk",
        "is_in_cart": True,
    }

    response2 = client.put(
        "/api/v1/lists/shopping/items/milk", json={"is_in_cart": True}
    )
    assert response2.status_code == 200
    assert response2.json() == {
        "id": 1,
        "list_id": 1,
        "name": "milk",
        "is_in_cart": True,
    }

    response3 = client.put(
        "/api/v1/lists/shopping/items/milk", json={"is_in_cart": True}
    )
    assert response3.status_code == 200
    assert response3.json() == {
        "id": 1,
        "list_id": 1,
        "name": "milk",
        "is_in_cart": True,
    }


def test_update_item_nonexistent(client):
    """Test updating a non-existent item fails"""
    # Create a list
    client.post("/api/v1/lists/shopping")
    # Try to update a non-existent item
    response = client.put(
        "/api/v1/lists/shopping/items/nonexistent", json={"is_in_cart": True}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
