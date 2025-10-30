from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models


async def get_manager_by_id(db: AsyncSession, manager_id: int) -> Optional[models.Manager]:
    result = await db.execute(select(models.Manager).where(models.Manager.id == manager_id))

    return result.scalar_one_or_none()




