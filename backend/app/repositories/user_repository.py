"""User repository."""

from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """User repository with custom queries."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, User)

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        stmt = select(self.model).where(self.model.email == email)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_by_email(self, email: str) -> User | None:
        """Get active user by email."""
        stmt = select(self.model).where(
            and_(self.model.email == email, self.model.status == "active")
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_active(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all active users (not deleted)."""
        stmt = (
            select(self.model)
            .where(self.model.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_pending(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all pending users."""
        stmt = (
            select(self.model)
            .where(and_(self.model.status == "pending", self.model.deleted_at.is_(None)))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def soft_delete(self, user_id: int) -> User | None:
        """Soft delete user."""
        user = await self.get(user_id)
        if not user:
            return None
        user.deleted_at = datetime.utcnow()
        self.db.add(user)
        await self.db.flush()
        return user

    async def get_all_students(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Get all students."""
        stmt = (
            select(self.model)
            .where(and_(self.model.role == "student", self.model.deleted_at.is_(None)))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_status(self, user_id: int, status: str) -> User | None:
        """Update user status."""
        user = await self.get(user_id)
        if not user:
            return None
        user.status = status
        user.updated_at = datetime.utcnow()
        self.db.add(user)
        await self.db.flush()
        return user
