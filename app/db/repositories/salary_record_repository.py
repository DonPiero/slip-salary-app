from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import models


async def get_salary_records_by_employee(db: AsyncSession, employee_id: int) -> Sequence[models.SalaryRecord]:
    result = await db.execute(select(models.SalaryRecord).where(models.SalaryRecord.employee_id == employee_id))

    return result.scalars().all()

