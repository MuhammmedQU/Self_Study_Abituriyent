"""Authentication service."""

from datetime import datetime, timedelta
from typing import Optional
import hashlib

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.user import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """Authentication service."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repo = UserRepository(db)
        self.token_repo = RefreshTokenRepository(db)

    async def register(
        self, full_name: str, email: str, password: str
    ) -> User | None:
        """Register new user (status=pending)."""
        # Check if user exists
        existing = await self.user_repo.get_by_email(email)
        if existing:
            return None

        # Validate password
        if not self._validate_password(password):
            return None

        # Create user with pending status
        user = await self.user_repo.create(
            {
                "full_name": full_name,
                "email": email,
                "password_hash": pwd_context.hash(password),
                "role": "student",
                "status": "pending",
            }
        )
        await self.user_repo.commit()
        return user

    async def login(self, email: str, password: str) -> dict | None:
        """Login user."""
        user = await self.user_repo.get_by_email(email)
        if not user or not pwd_context.verify(password, user.password_hash):
            return None

        # Check if account is active
        if user.status != "active":
            return None

        # Generate tokens
        access_token = self._create_access_token(user.id, user.email)
        refresh_token = await self._create_refresh_token(user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": user.id,
            "email": user.email,
        }

    async def refresh_access_token(self, refresh_token: str) -> dict | None:
        """Refresh access token and rotate refresh token."""
        # Verify refresh token
        token_data = self._verify_token(
            refresh_token, settings.jwt_refresh_secret
        )
        if not token_data:
            return None

        user_id = token_data.get("sub")
        if not user_id:
            return None

        # Check if token is revoked
        token_record = await self.token_repo.get_by_token_hash(
            self._hash_token(refresh_token)
        )
        if not token_record or token_record.revoked_at:
            return None

        # Get user
        user = await self.user_repo.get(user_id)
        if not user or user.deleted_at:
            return None

        # Revoke old token
        await self.token_repo.revoke_token(self._hash_token(refresh_token))

        # Generate new tokens
        new_access_token = self._create_access_token(user.id, user.email)
        new_refresh_token = await self._create_refresh_token(user.id)

        await self.token_repo.commit()

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }

    async def logout(self, refresh_token: str) -> bool:
        """Logout - revoke refresh token."""
        await self.token_repo.revoke_token(self._hash_token(refresh_token))
        await self.token_repo.commit()
        return True

    async def verify_token(self, token: str) -> dict | None:
        """Verify access token and return user data."""
        data = self._verify_token(token, settings.jwt_secret)
        if not data:
            return None

        user_id = data.get("sub")
        email = data.get("email")

        if not user_id:
            return None

        user = await self.user_repo.get(user_id)
        if not user or user.deleted_at:
            return None

        return {"user_id": user_id, "email": email, "role": user.role}

    def _validate_password(self, password: str) -> bool:
        """Validate password requirements."""
        if len(password) < 8:
            return False
        if not any(c.isalpha() for c in password):
            return False
        if not any(c.isdigit() for c in password):
            return False
        return True

    def _create_access_token(self, user_id: int, email: str) -> str:
        """Create access token."""
        expires = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        data = {"sub": user_id, "email": email, "exp": expires}
        return jwt.encode(data, settings.jwt_secret, algorithm="HS256")

    async def _create_refresh_token(self, user_id: int) -> str:
        """Create refresh token."""
        expires = datetime.utcnow() + timedelta(
            days=settings.refresh_token_expire_days
        )
        token = jwt.encode(
            {"sub": user_id, "exp": expires},
            settings.jwt_refresh_secret,
            algorithm="HS256",
        )

        # Store token hash
        await self.token_repo.create(
            {
                "user_id": user_id,
                "token_hash": self._hash_token(token),
                "expires_at": expires,
            }
        )

        return token

    def _verify_token(self, token: str, secret: str) -> dict | None:
        """Verify JWT token."""
        try:
            return jwt.decode(token, secret, algorithms=["HS256"])
        except JWTError:
            return None

    def _hash_token(self, token: str) -> str:
        """Hash token for storage."""
        return hashlib.sha256(token.encode()).hexdigest()
