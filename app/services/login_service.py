from sqlalchemy.ext.asyncio import AsyncSession

from app.db.repositories.user_repository import get_user_by_email
from app.core.security import verify_password, create_access_token
from app.core.loging import logger


async def login(db: AsyncSession, email: str, password: str) -> dict | None:
    try:
        user = await get_user_by_email(db, email)
        if not user:
            logger.warning(f"No user found for email: {email}")
            return None

        if not verify_password(password, user.password):
            logger.warning(f"Wrong password for email: {email}")
            return None

        payload = {
            "sub": user.email,
            "role": user.role,
        }

        token = create_access_token(payload)
        if not token:
            logger.error("Token generation failed during login.")
            return None

        return {"access_token": token, "token_type": "bearer", "role": user.role}

    except Exception as e:
        logger.error(f"Unexpected error for logging: {email}: {e}")
        return None
