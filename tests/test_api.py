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
    assert response.json() == {"message": "List 'todo' created successfully"}


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
