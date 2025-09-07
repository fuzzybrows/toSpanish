import pytest
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware

from app.server import app


def test_app_instance():
    """Test that the app instance is created correctly."""
    assert app is not None
    assert app.title == "FastAPI"  # Default title


def test_router_included():
    """Test that the router is included in the app."""
    # Check that the router paths are included in the app routes
    route_paths = [route.path for route in app.routes]
    
    # Check for some expected routes
    assert "/" in route_paths
    assert "/propresenter/include_spanish" in route_paths
    assert "/propresenter/upload_exported_files" in route_paths
    assert "/propresenter/download_importable_file/{file_id}" in route_paths