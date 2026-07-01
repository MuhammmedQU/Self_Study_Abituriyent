"""Activity log repository."""

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity_log import ActivityLog
from app.repositories.base import BaseRepository


class ActivityLogRepository(BaseRepository[ActivityLog]):
    """Activity log repository."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, ActivityLog)

    async def get_recent(self, skip: int = 0, limit: int = 100) -> list[ActivityLog]:
        """Get recent activity logs."""
        stmt = (
            select(self.model)
            .order_by(desc(self.model.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_user_activity(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[ActivityLog]:
        """Get activity logs for user."""
        stmt = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(desc(self.model.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
