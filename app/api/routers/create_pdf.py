from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_role
from app.api.errors import error_500, error_404, error_409
from app.db.repositories.employee_repository import get_employees_by_manager
from app.services.pdf_service import generate_pdf
from app.utils.idempotency import check_duplicate

router = APIRouter(prefix="", tags=["pdf"])


@router.post("/createPdfForEmployees")
async def create_pdf_for_employees(current_manager = Depends(get_role), db: AsyncSession = Depends(get_db)):
    try:
        if check_duplicate(current_manager.id, "pdf", "create"):
            error_409("For this manager, the PDF files have already been created for this month.")

        employees = await get_employees_by_manager(db, current_manager.id)
        if not employees:
            error_404("No employees or salary records found for this manager.")

        for employee in employees:
            await generate_pdf(db, employee.id)

        return

    except HTTPException:
        raise

    except Exception as e:
        error_500(f"Error generating PDFs for manager {current_manager.email}: {e}")
