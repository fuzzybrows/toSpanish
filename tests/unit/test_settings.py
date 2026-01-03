import os
import pytest
from unittest.mock import patch
from pydantic import ValidationError

from app.settings import Settings, ROOT_DIR, PROJECT_DIR, settings
from app.schema import GeminiModels


def test_root_dir_and_project_dir():
    """Test that ROOT_DIR and PROJECT_DIR are set correctly."""
    assert ROOT_DIR == os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    assert PROJECT_DIR == f"{ROOT_DIR}/app"


@patch.dict(os.environ, {
    "environment": "test",
    "database_url": "postgresql://user:password@localhost:5432/test_db",
    "genai_client_api_key": "test_api_key",
    "port": "5005"
})
def test_settings_from_env():
    """Test that settings are loaded from environment variables."""
    settings = Settings()
    assert settings.environment == "test"
    assert settings.database_url == "postgresql://user:password@localhost:5432/test_db"
    assert settings.genai_client_api_key == "test_api_key"
    assert settings.port == 5005
    assert settings.root_dir == ROOT_DIR
    assert settings.project_dir == PROJECT_DIR


@patch.dict(os.environ, {
    "environment": "local",
    "database_url": "postgresql://user:password@localhost:5432/test_db",
    "genai_client_api_key": "test_api_key",
    "allowed_origins": "http://localhost:3000|https://example.com"
})
def test_get_allowed_origins_with_origins():
    """Test that get_allowed_origins returns a list of origins when allowed_origins is set."""
    settings = Settings()
    assert settings.get_allowed_origins == ["http://localhost:3000", "https://example.com"]


@patch.dict(os.environ, {
    "environment": "local",
    "database_url": "postgresql://user:password@localhost:5432/test_db",
    "genai_client_api_key": "test_api_key",
    "allowed_origins": ""
})
def test_get_allowed_origins_local_environment():
    """Test that get_allowed_origins returns ['*'] when environment is local and allowed_origins is not set."""
    settings = Settings()
    assert settings.get_allowed_origins == ["*"]


@patch.dict(os.environ, {
    "environment": "production",
    "database_url": "postgresql://user:password@localhost:5432/test_db",
    "genai_client_api_key": "test_api_key",
    "allowed_origins": ""
})
def test_get_allowed_origins_production_environment():
    """Test that get_allowed_origins returns an empty list when environment is not local and allowed_origins is not set."""
    settings = Settings()
    assert settings.get_allowed_origins == []


@patch.dict(os.environ, {
    "environment": "test",
    "database_url": "postgresql://user:password@localhost:5432/test_db",
    "genai_client_api_key": "test_api_key",
    "model_name": "TWO_FLASH"
})
def test_strict_model_names_only_valid_string():
    """Test that a valid model name string is accepted."""
    settings = Settings()
    assert settings.model_name == GeminiModels.TWO_FLASH


@patch.dict(os.environ, {
    "environment": "test",
    "database_url": "postgresql://user:password@localhost:5432/test_db",
    "genai_client_api_key": "test_api_key",
    "model_name": "INVALID_MODEL"
})
def test_strict_model_names_only_invalid_string():
    """Test that an invalid model name string raises a ValidationError."""
    with pytest.raises(ValidationError) as excinfo:
        Settings()
    assert "Invalid name. Must be one of:" in str(excinfo.value)


def test_strict_model_names_only_enum_instance():
    """Test that a valid GeminiModels enum instance is accepted."""
    settings = Settings(
        environment="test",
        database_url="postgresql://user:password@localhost:5432/test_db",
        genai_client_api_key="test_api_key",
        model_name=GeminiModels.TWO_FLASH
    )
    assert settings.model_name == GeminiModels.TWO_FLASH
