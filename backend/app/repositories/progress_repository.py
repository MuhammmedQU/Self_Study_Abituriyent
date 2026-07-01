"""Progress repository."""

from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.progress import Progress
from app.repositories.base import BaseRepository


class ProgressRepository(BaseRepository[Progress]):
    """Progress repository."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Progress)

    async def get_user_module_progress(
        self, user_id: int, module_id: int
    ) -> Progress | None:
        """Get progress for user in module."""
        stmt = select(self.model).where(
            and_(self.model.user_id == user_id, self.model.module_id == module_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_all_progress(self, user_id: int) -> list[Progress]:
        """Get all progress for user."""
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def create_or_update(
        self, user_id: int, module_id: int, data: dict
    ) -> Progress:
        """Create or update progress."""
        progress = await self.get_user_module_progress(user_id, module_id)
        if progress:
            for key, value in data.items():
                setattr(progress, key, value)
            progress.updated_at = datetime.utcnow()
            self.db.add(progress)
        else:
            progress = Progress(user_id=user_id, module_id=module_id, **data)
            self.db.add(progress)
        await self.db.flush()
        return progress

    async def update_activity(self, user_id: int, module_id: int) -> Progress | None:
        """Update last activity."""
        progress = await self.get_user_module_progress(user_id, module_id)
        if progress:
            progress.last_activity = datetime.utcnow()
            self.db.add(progress)
            await self.db.flush()
        return progress
