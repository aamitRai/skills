"""
Application configuration management.

Centralized settings loaded from environment variables via Pydantic BaseSettings.
"""

from pathlib import Path

from pydantic_settings import BaseSettings

# Resolve .env relative to this file's location (backend/.env)
ENV_FILE = Path(__file__).resolve().parent.parent.parent / ".env"


class Settings(BaseSettings):
    """Application-wide configuration loaded from environment variables."""

    # MongoDB
    MONGODB_URI: str
    MONGODB_DB_NAME: str

    # Security
    SECRET_KEY: str = "change-me-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"

    # CORS
    ALLOWED_ORIGINS: str = "*"

    # Server
    APP_NAME: str = "Skills Tracker API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    model_config = {
        "env_file": str(ENV_FILE),
        "env_file_encoding": "utf-8",
    }


settings = Settings()
