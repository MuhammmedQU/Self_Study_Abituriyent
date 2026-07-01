"""Course repository."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course
from app.repositories.base import BaseRepository


class CourseRepository(BaseRepository[Course]):
    """Course repository."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Course)

    async def get_all_active(self, skip: int = 0, limit: int = 100) -> list[Course]:
        """Get all active courses (not deleted)."""
        stmt = (
            select(self.model)
            .where(self.model.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_by_title(self, title: str) -> Course | None:
        """Get course by title."""
        stmt = select(self.model).where(
            self.model.title == title, self.model.deleted_at.is_(None)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def soft_delete(self, course_id: int) -> Course | None:
        """Soft delete course (cascade to modules, lessons, resources)."""
        from datetime import datetime
        course = await self.get(course_id)
        if not course:
            return None
        course.deleted_at = datetime.utcnow()
        self.db.add(course)
        await self.db.flush()
        return course
