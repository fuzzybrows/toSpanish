import os

from pydantic_settings import SettingsConfigDict, BaseSettings
from pydantic import field_validator

from app.schema import GeminiModels

ROOT_DIR = f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}"
PROJECT_DIR = f"{ROOT_DIR}/app"

class Settings(BaseSettings):
    environment: str
    root_dir: str = ROOT_DIR
    project_dir: str = PROJECT_DIR
    genai_client_api_key: str
    model_name: GeminiModels = GeminiModels.TWO_FLASH
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

    @field_validator("model_name", mode="before")
    @classmethod
    def strict_names_only(cls, v):
        try:
            return GeminiModels[v]
        except KeyError:
            raise ValueError(f"Invalid name. Must be one of: {list(GeminiModels.__members__.keys())}")


settings = Settings()