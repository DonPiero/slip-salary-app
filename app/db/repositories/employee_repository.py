from collections.abc import Sequence
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models


async def get_employee_by_id(db: AsyncSession, employee_id: int) -> Optional[models.Employee]:
    result = await db.execute(select(models.Employee).where(models.Employee.id == employee_id))

    return result.scalar_one_or_none()

async def get_employees_by_manager(db: AsyncSession, manager_id: int) -> Sequence[models.Employee]:
    result = await db.execute(select(models.Employee).where(models.Employee.manager_id == manager_id))

    return result.scalars().all()
