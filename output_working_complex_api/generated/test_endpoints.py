"""
Test suite for the generated Pet Service API.
This tests the endpoints without requiring an external service.
"""
import pytest
import sys
import os
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

# Add the current directory to sys.path to allow imports
sys.path.insert(0, os.path.dirname(__file__))

# Import the app
from main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_create_pet_success(client):
    """Test successful pet creation."""
    with patch("clients.pet_client.PetServiceClient.create_pet", new_callable=AsyncMock) as mock_create:
        response = client.post("/pets", json={"content": "Fluffy the cat"})
        assert response.status_code == 201
        mock_create.assert_called_once()


def test_create_pet_empty_content(client):
    """Test that empty content is rejected."""
    response = client.post("/pets", json={"content": ""})
    assert response.status_code == 422  # Validation error


def test_create_pet_missing_content(client):
    """Test that missing content field is rejected."""
    response = client.post("/pets", json={})
    assert response.status_code == 422  # Validation error


def test_create_pet_whitespace_only(client):
    """Test that whitespace-only content is rejected."""
    response = client.post("/pets", json={"content": "   "})
    assert response.status_code == 422  # Validation error


def test_openapi_docs(client):
    """Test that OpenAPI documentation is available."""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower()


def test_redoc_docs(client):
    """Test that ReDoc documentation is available."""
    response = client.get("/redoc")
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
