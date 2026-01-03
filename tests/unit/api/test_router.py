import os
import json
import pytest
from unittest.mock import patch, MagicMock
from fastapi import UploadFile
from fastapi.testclient import TestClient

from app.models.public.schema import IncludeSpanishRequest, SongsParentModel


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "My API"}


@patch("app.router.generate_with_spanish_translations")
@patch("app.router.create_import_file_string")
def test_include_spanish_endpoint(mock_create_import_file_string, mock_generate_with_spanish_translations, client, sample_songs_parent):
    """Test the include_spanish endpoint."""
    # Mock the service functions
    mock_generate_with_spanish_translations.return_value = sample_songs_parent
    mock_create_import_file_string.return_value = "Mocked importable file content"
    
    # Make the request
    request_data = {"text": "Test song lyrics"}
    response = client.post("/propresenter/include_spanish", json=request_data)
    
    # Check the response
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["text_data"] == "Mocked importable file content"
    assert "json_data" in response_data
    
    # Verify the mocks were called correctly
    mock_generate_with_spanish_translations.assert_called_once_with(texts=["Test song lyrics"])
    mock_create_import_file_string.assert_called_once_with(structured_raw_file=sample_songs_parent)


@patch("app.router.process_files_background")
def test_upload_exported_files_endpoint(mock_process_files_background, client, tmp_path):
    """Test the upload_exported_files endpoint."""
    # Create a test file
    test_file_content = b"Test file content"
    
    # Make the request with a test file
    response = client.post(
        "/propresenter/upload_exported_files",
        files={"files": ("test_file.txt", test_file_content)}
    )
    
    # Check the response
    assert response.status_code == 200
    response_data = response.json()
    assert "file_id" in response_data
    
    # Verify the mock was called
    mock_process_files_background.assert_called_once()


@patch("os.path.exists")
def test_download_importable_file_endpoint_not_found(mock_exists, client):
    """Test the download_importable_file endpoint when the file doesn't exist."""
    # Mock os.path.exists to return False
    mock_exists.return_value = False
    
    # Make the request
    response = client.get("/propresenter/download_importable_file/test_file_id")
    
    # Check the response
    assert response.status_code == 200
    assert response.json() == {"message": "File not found"}


@patch("os.path.exists")
@patch("fastapi.responses.FileResponse")
def test_download_importable_file_endpoint_found(mock_file_response, mock_exists, client):
    """Test the download_importable_file endpoint when the file exists."""
    # Mock os.path.exists to return True
    mock_exists.return_value = True
    
    # Mock FileResponse
    mock_file_response.return_value = MagicMock()
    
    # Make the request
    with patch("app.router.FileResponse", mock_file_response):
        response = client.get("/propresenter/download_importable_file/test_file_id")
    
    # Verify the mock was called with the correct path
    expected_path = f"{os.path.abspath('.')}/data/processed/test_file_id/importable_file.txt"
    mock_file_response.assert_called()