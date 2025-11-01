from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_role
from app.api.errors import error_400, error_409, error_500
from app.services.archive_service import archive_exported_files
from app.services.email_service import send_email
from app.utils.idempotency import check_creation, check_duplicate, check_archivable

router = APIRouter(prefix="", tags=["csv"])


@router.post("/sendAggregatedEmployeeData")
async def send_aggregated_employee_data(current_manager = Depends(get_role)):
    try:
        if not check_creation(current_manager.id, "csv"):
            error_400("The file has not been created yet.")

        if check_duplicate(current_manager.id, "csv", "send"):
            error_409("The file has already been sent this month.")

        send_email("manager", current_manager.email, current_manager.id, current_manager.id)
        if check_archivable(current_manager.id):
            archive_exported_files(current_manager.id)

        return

    except HTTPException:
        raise

    except Exception as e:
        error_500(f"Error sending CSV for {current_manager.email}, error: {e}")
