#!/usr/bin/env python3
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from eggs.api import app
from fastapi.testclient import TestClient


def test_api():
    client = TestClient(app)

    # Test the endpoint
    response = client.get("/api/v1/lists/")
    assert response.status_code == 200
    assert response.json() == []

    print("API test passed!")


if __name__ == "__main__":
    test_api()
