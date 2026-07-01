"""Lesson repository."""

from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lesson import Lesson
from app.repositories.base import BaseRepository


class LessonRepository(BaseRepository[Lesson]):
    """Lesson repository."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Lesson)

    async def get_by_module(
        self, module_id: int, skip: int = 0, limit: int = 100
    ) -> list[Lesson]:
        """Get all lessons for a module."""
        stmt = (
            select(self.model)
            .where(and_(self.model.module_id == module_id, self.model.deleted_at.is_(None)))
            .order_by(self.model.order)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def soft_delete(self, lesson_id: int, deleted_by: str) -> Lesson | None:
        """Soft delete lesson."""
        lesson = await self.get(lesson_id)
        if not lesson:
            return None
        lesson.deleted_at = datetime.utcnow()
        lesson.deleted_by = deleted_by
        self.db.add(lesson)
        await self.db.flush()
        return lesson

    async def get_next_lesson(self, module_id: int, current_order: int) -> Lesson | None:
        """Get next lesson in module."""
        stmt = (
            select(self.model)
            .where(
                and_(
                    self.model.module_id == module_id,
                    self.model.order > current_order,
                    self.model.deleted_at.is_(None),
                )
            )
            .order_by(self.model.order)
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
