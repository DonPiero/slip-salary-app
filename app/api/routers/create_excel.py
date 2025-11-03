from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_manager
from app.api.errors import error_409, error_404, error_500
from app.services.csv_service import generate_csv
from app.utils.idempotency import check_duplicate

router = APIRouter(prefix="", tags=["csv"])


@router.post("/createAggregatedEmployeeData")
async def create_aggregated_employee_data(current_manager = Depends(get_manager), db: AsyncSession = Depends(get_db)):
    try:
        if check_duplicate(current_manager.id, "csv", "create"):
            error_409("For this manager, the CSV file has already been created for this month.")

        csv_path = await generate_csv(db, current_manager.id)
        if not csv_path:
            error_404("No employees or salary records found for this manager.")

        return

    except HTTPException:
        raise

    except Exception as e:
        error_500(f"Error generating CSV for {current_manager.email}: {e}")
