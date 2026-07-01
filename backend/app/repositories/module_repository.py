"""Module repository."""

from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.module import Module
from app.repositories.base import BaseRepository


class ModuleRepository(BaseRepository[Module]):
    """Module repository."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Module)

    async def get_by_course(
        self, course_id: int, skip: int = 0, limit: int = 100
    ) -> list[Module]:
        """Get all modules for a course."""
        stmt = (
            select(self.model)
            .where(and_(self.model.course_id == course_id, self.model.deleted_at.is_(None)))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def soft_delete(self, module_id: int, deleted_by: str) -> Module | None:
        """Soft delete module and cascade to lessons."""
        module = await self.get(module_id)
        if not module:
            return None
        module.deleted_at = datetime.utcnow()
        module.deleted_by = deleted_by
        self.db.add(module)
        await self.db.flush()
        return module
