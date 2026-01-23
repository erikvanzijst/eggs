from eggs.api import app
from fastapi.testclient import TestClient


def test_api():
    client = TestClient(app)

    # Test the endpoint
    response = client.get("/api/v1/lists/")
    assert response.status_code == 200
    assert response.json() == []
