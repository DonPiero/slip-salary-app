from fastapi import HTTPException, status

from app.core.loging import logger


def error_400(detail: str):
    logger.warning(detail)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def error_401(detail: str):
    logger.warning(detail)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


def error_403(detail: str):
    logger.warning(detail)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


def error_404(detail: str):
    logger.warning(detail)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def error_409(detail: str):
    logger.warning(detail)
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


def error_500(detail: str):
    logger.error(detail)
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
