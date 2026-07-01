"""Announcement repository."""

from datetime import datetime

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.announcement import Announcement
from app.repositories.base import BaseRepository


class AnnouncementRepository(BaseRepository[Announcement]):
    """Announcement repository."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Announcement)

    async def get_all_active(
        self, skip: int = 0, limit: int = 100
    ) -> list[Announcement]:
        """Get all active announcements (not deleted)."""
        stmt = (
            select(self.model)
            .where(self.model.deleted_at.is_(None))
            .order_by(desc(self.model.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def soft_delete(self, announcement_id: int) -> Announcement | None:
        """Soft delete announcement."""
        announcement = await self.get(announcement_id)
        if announcement:
            announcement.deleted_at = datetime.utcnow()
            self.db.add(announcement)
            await self.db.flush()
        return announcement
