from datetime import datetime
from decimal import Decimal
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.core.loging import logger
from app.db.repositories.employee_repository import get_employee_by_id
from app.db.repositories.salary_record_repository import get_salary_records_by_employee
from app.services.encryption_service import encrypt_pdf


async def generate_pdf(db: AsyncSession, employee_id: int) -> Path | None:
    try:
        now = datetime.now()
        month = now.month
        year = now.year

        employee = await get_employee_by_id(db, employee_id)
        if not employee:
            logger.warning(f"No employee found with ID: {employee_id}")
            return None

        salary_records = await get_salary_records_by_employee(db, employee_id)
        if not salary_records:
            logger.warning(f"No salary records found for employee with ID: {employee_id}")
            return None

        salary = next((s for s in salary_records if s.month == month and s.year == year), None)

        export_directory = Path(__file__).resolve().parents[2] / "data" / "export" / f"manager_{employee.manager_id}" / "pdf"
        export_directory.mkdir(parents=True, exist_ok=True)
        file_path = export_directory / f"employee_{employee.id}.pdf"

        c = canvas.Canvas(str(file_path), pagesize=A4)
        width, height = A4
        y = height - 80

        c.setFont("Helvetica-Bold", 18)
        c.drawString(200, y, "Monthly Payslip")
        y -= 50

        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Name: {employee.name} {employee.surname}")
        y -= 20
        c.drawString(50, y, f"Employee ID: {employee.id}")
        y -= 20
        c.drawString(50, y, f"CNP: {employee.cnp}")
        y -= 20
        c.drawString(50, y, f"Email: {employee.email}")
        y -= 40

        c.drawString(50, y, f"Month: {salary.month}/{salary.year}")
        y -= 20
        c.drawString(50, y, f"Working Days: {salary.working_days}")
        y -= 20
        c.drawString(50, y, f"Vacation Days: {salary.vacation_days}")
        y -= 20
        c.drawString(50, y, f"Base Salary: {salary.base_salary:.2f}")
        y -= 20
        c.drawString(50, y, f"Bonuses: {salary.bonuses or Decimal('0.00'):.2f}")
        y -= 40

        total = salary.base_salary + (salary.bonuses or Decimal("0.00"))
        c.drawString(50, y, f"Total to be paid: {total:.2f}")
        c.save()

        if not encrypt_pdf(file_path, employee.cnp):
            logger.warning(f"PDF generated, but encryption failed for: {employee.id}")
            return None

        logger.warning(f"PDF files generated for employee {employee_id}.")
        return file_path

    except Exception as e:
        logger.error(f"Failed to generate PDF for employee: {employee_id}, with error: {e}")
        return None
