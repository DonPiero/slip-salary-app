from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.errors import error_401, error_404, error_500, error_403
from app.db.session import session
from app.core.security import decode_access_token
from app.db.repositories.user_repository import get_user_by_email

user_token = OAuth2PasswordBearer(tokenUrl="/login")

async def get_db():
    db = session()
    try:
        yield db

    except Exception as e:
        error_500(f"Database session error: {e}")

    finally:
        await db.close()


async def get_user(token: str = Depends(user_token), db: AsyncSession = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        if not payload:
            error_401("Invalid or expired token.")

        email = payload.get("sub")
        if not email:
            error_401("Email field missing.")

        user = await get_user_by_email(db, email)
        if not user:
            error_404("User not found.")

        return user

    except HTTPException:
        raise
    except Exception as e:
        error_500(f"Error retrieving user from token: {e}")


async def get_role(user=Depends(get_user)):
    try:
        if user.role != "manager":
            error_403("Insufficient permissions for this action.")
        return user

    except HTTPException:
        raise

    except Exception as e:
        error_500(f"Error verifying user's permissions: {e}")
