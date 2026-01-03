from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.server import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test that the root endpoint returns the expected response."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "My API"}


@patch('app.service.get_gemini_response', side_effect=Exception())
def test_include_spanish_endpoint_validation(mock_get_gemini_response, client):
    """Test that the include_spanish endpoint validates the request body."""
    # Test with missing required field
    response = client.post("/propresenter/include_spanish", json={})
    assert response.status_code == 422  # Unprocessable Entity
    
    # Test with valid request body (but mocked service)
    with pytest.raises(Exception):
        response = client.post("/propresenter/include_spanish", json={"text": "Test text"})

    mock_get_gemini_response.assert_called_once()


def test_download_importable_file_not_found(client):
    """Test that the download_importable_file endpoint returns a not found message when the file doesn't exist."""
    response = client.get("/propresenter/download_importable_file/non_existent_file_id")
    assert response.status_code == 200
    assert response.json() == {"message": "File not found"}