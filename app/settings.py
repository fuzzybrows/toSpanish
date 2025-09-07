import os

from pydantic_settings import SettingsConfigDict, BaseSettings

ROOT_DIR = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}"
PROJECT_DIR = f"{ROOT_DIR}/app"

class Settings(BaseSettings):
    environment: str
    database_url: str
    root_dir: str = ROOT_DIR
    project_dir: str = PROJECT_DIR
    genai_client_api_key: str
    port: int = 9000
    allowed_origins: str | None = None

    model_config = SettingsConfigDict(extra="ignore", env_file=f"{ROOT_DIR}/.env")

    @property
    def get_allowed_origins(self):
        if self.allowed_origins is not None:
            return self.allowed_origins.split("|")
        if self.environment == "local":
            return ["*"]
        return []


settings = Settings()