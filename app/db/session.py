from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings
from app.core.logging import logger

try:
    engine = create_async_engine(settings.database_async, echo=True)
    session = async_sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
except Exception as e:
    logger.error(f"Failed to create the engine for database: {e}")
