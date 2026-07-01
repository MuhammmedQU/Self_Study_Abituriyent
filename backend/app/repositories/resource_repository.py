"""Resource repository."""

from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.resource import Resource
from app.repositories.base import BaseRepository


class ResourceRepository(BaseRepository[Resource]):
    """Resource repository."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Resource)

    async def get_by_lesson(self, lesson_id: int) -> list[Resource]:
        """Get all resources for a lesson."""
        stmt = select(self.model).where(
            and_(self.model.lesson_id == lesson_id, self.model.deleted_at.is_(None))
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def soft_delete(self, resource_id: int, deleted_by: str) -> Resource | None:
        """Soft delete resource."""
        resource = await self.get(resource_id)
        if not resource:
            return None
        resource.deleted_at = datetime.utcnow()
        resource.deleted_by = deleted_by
        self.db.add(resource)
        await self.db.flush()
        return resource
