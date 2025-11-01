from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors import error_401, error_500
from app.services.login_service import login
from app.api.schemas import Request, Response
from app.api.deps import get_db


router = APIRouter(prefix="", tags=["auth"])

@router.post("/login", response_model=Response)
async def login_user(data: Request, db: AsyncSession = Depends(get_db)):
    try:
        login_data = await login(db, data.email, data.password)
        if not login_data:
            error_401("Login failed. Please try again.")

        return login_data

    except HTTPException:
        raise

    except Exception as e:
        error_500(f"Failed login for {data.email}, error: {e}")
