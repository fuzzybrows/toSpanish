import os

from pydantic_settings import SettingsConfigDict, BaseSettings

ROOT_DIR = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}"
PROJECT_DIR = f"{ROOT_DIR}/app"

class Settings(BaseSettings):
    environment: str
    root_dir: str = ROOT_DIR
    project_dir: str = PROJECT_DIR
    genai_client_api_key: str
    port: int = 9000

    model_config = SettingsConfigDict(extra="ignore", env_file=f"{ROOT_DIR}/.env")

settings = Settings()