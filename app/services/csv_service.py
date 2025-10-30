from datetime import datetime
from decimal import Decimal
from pathlib import Path
import csv
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.loging import logger
from app.db.repositories.employee_repository import get_employees_by_manager
from app.db.repositories.salary_record_repository import get_salary_records_by_employee


async def generate_csv(db: AsyncSession, manager_id: int) -> Path | None:
    try:
        now = datetime.now()
        month = now.month
        year = now.year

        employees = await get_employees_by_manager(db, manager_id)
        if not employees:
            logger.warning(f"No employees found for manager ID: {manager_id}")
            return None

        export_directory = Path(__file__).resolve().parents[2] / "data" / "export" / "csv"
        export_directory.mkdir(parents=True, exist_ok=True)
        file_path = export_directory / f"manager_{manager_id}.csv"

        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Employee Name", "Email",
                "Base Salary", "Bonuses", "Total Salary",
                "Working Days", "Vacation Days"
            ])

            for emp in employees:
                salary_records = await get_salary_records_by_employee(db, emp.id)
                salary = next((s for s in salary_records if s.month == month and s.year == year), None)
                if not salary:
                    continue

                total = salary.base_salary + (salary.bonuses or Decimal("0.00"))
                writer.writerow([
                    f"{emp.name} {emp.surname}",
                    emp.email,
                    f"{salary.base_salary:.2f}",
                    f"{salary.bonuses or Decimal('0.00'):.2f}",
                    f"{total:.2f}",
                    salary.working_days,
                    salary.vacation_days
                ])

        return file_path

    except Exception as e:
        logger.error(f"Failed to generate CSV for manager: {manager_id}, with error: {e}")
        return None
