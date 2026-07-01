"""Dependency injection."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.auth_service import AuthService

security = HTTPBearer()


async def get_current_user(
    credentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Get current authenticated user."""
    token = credentials.credentials
    auth_service = AuthService(db)
    user_data = await auth_service.verify_token(token)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return user_data


async def require_admin(
    user: dict = Depends(get_current_user),
) -> dict:
    """Require admin role."""
    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user


async def require_student(
    user: dict = Depends(get_current_user),
) -> dict:
    """Require student role."""
    if user.get("role") != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Student access required",
        )
    return user
