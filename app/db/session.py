from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.database_async, echo=True)
session = async_sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
