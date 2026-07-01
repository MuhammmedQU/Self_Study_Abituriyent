"""Base repository with generic CRUD operations."""

from typing import Generic, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    """Base repository for all models."""

    def __init__(self, db: AsyncSession, model: Type[T]):
        self.db = db
        self.model = model

    async def create(self, obj_in: dict) -> T:
        """Create a new record."""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def get(self, id: int) -> T | None:
        """Get a record by ID."""
        stmt = select(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        """Get all records with pagination."""
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update(self, id: int, obj_in: dict) -> T | None:
        """Update a record."""
        db_obj = await self.get(id)
        if not db_obj:
            return None
        for key, value in obj_in.items():
            setattr(db_obj, key, value)
        self.db.add(db_obj)
        await self.db.flush()
        return db_obj

    async def delete(self, id: int) -> bool:
        """Hard delete a record."""
        db_obj = await self.get(id)
        if not db_obj:
            return False
        await self.db.delete(db_obj)
        await self.db.flush()
        return True

    async def commit(self) -> None:
        """Commit transaction."""
        await self.db.commit()

    async def rollback(self) -> None:
        """Rollback transaction."""
        await self.db.rollback()
