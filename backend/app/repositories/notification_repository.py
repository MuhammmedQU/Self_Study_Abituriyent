"""Notification repository."""

from sqlalchemy import and_, select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    """Notification repository."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Notification)

    async def get_user_notifications(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> list[Notification]:
        """Get all notifications for user."""
        stmt = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(desc(self.model.created_at))
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def mark_as_read(self, notification_id: int) -> Notification | None:
        """Mark notification as read."""
        notification = await self.get(notification_id)
        if notification:
            notification.is_read = True
            self.db.add(notification)
            await self.db.flush()
        return notification
