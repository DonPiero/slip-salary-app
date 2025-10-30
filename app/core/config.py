from pydantic_settings import BaseSettings

from app.core.logging import logger


class Settings(BaseSettings):
    database_async: str
    database_sync: str

    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expiration_minutes: int

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str

    class Config:
        env_file = ".env"

try:
    settings = Settings()
except Exception as e:
    logger.error(f"Failed to load settings: {e}")
