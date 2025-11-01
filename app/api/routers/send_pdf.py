from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_role
from app.api.errors import error_400, error_409, error_404, error_500
from app.db.repositories.employee_repository import get_employees_by_manager
from app.services.archive_service import archive_exported_files
from app.services.email_service import send_email
from app.utils.idempotency import check_creation, check_duplicate, check_archivable

router = APIRouter(prefix="", tags=["pdf"])


@router.post("/sendPdfToEmployees")
async def send_pdf_to_employees(current_manager = Depends(get_role), db: AsyncSession = Depends(get_db)):
    try:
        if not check_creation(current_manager.id, "pdf"):
            error_400("The files have not been created yet.")

        if check_duplicate(current_manager.id, "pdf", "send"):
            error_409("The files have already been sent this month.")

        employees = await get_employees_by_manager(db, current_manager.id)
        if not employees:
            error_404("No employees or salary records found for this manager.")

        for e in employees:
            send_email("employee", e.email, current_manager.id, e.id)

        if check_archivable(current_manager.id):
            archive_exported_files(current_manager.id)

        return

    except HTTPException:
        raise

    except Exception as e:
        error_500(f"Error sending PDFs for manager {current_manager.email}: {e}")
