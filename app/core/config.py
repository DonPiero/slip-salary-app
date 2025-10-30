from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from app.core.loging import logger


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parents[2] / ".env")

    database_async: str
    database_sync: str

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expiration_minutes: int

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str


try:
    settings = Settings()
except Exception as e:
    logger.error(f"Failed to load settings: {e}")
