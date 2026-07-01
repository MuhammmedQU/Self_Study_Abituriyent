"""Auth router."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)


@router.post("/register")
async def register(
    payload: RegisterRequest, db: AsyncSession = Depends(get_db)
):
    """Register new user."""
    auth_service = AuthService(db)
    user = await auth_service.register(
        full_name=payload.full_name,
        email=payload.email,
        password=payload.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed. Email may already exist or password is invalid.",
        )

    return {
        "success": True,
        "message": "Registration successful. Wait for admin approval.",
        "data": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
        },
    }


@router.post("/login")
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Login user."""
    auth_service = AuthService(db)
    result = await auth_service.login(email=payload.email, password=payload.password)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or account not active",
        )

    return {
        "success": True,
        "message": "Login successful",
        "data": result,
    }


@router.post("/refresh")
async def refresh(
    payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)
):
    """Refresh access token."""
    auth_service = AuthService(db)
    result = await auth_service.refresh_access_token(payload.refresh_token)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    return {
        "success": True,
        "message": "Token refreshed",
        "data": result,
    }


@router.post("/logout")
async def logout(
    credentials: HTTPAuthCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
):
    """Logout user."""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token required",
        )

    auth_service = AuthService(db)
    await auth_service.logout(credentials.credentials)

    return {
        "success": True,
        "message": "Logout successful",
    }
