"""Quiz attempt repository."""

from sqlalchemy import and_, select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.quiz_attempt import QuizAttempt
from app.repositories.base import BaseRepository


class QuizAttemptRepository(BaseRepository[QuizAttempt]):
    """Quiz attempt repository."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, QuizAttempt)

    async def get_user_attempts(
        self, user_id: int, quiz_id: int
    ) -> list[QuizAttempt]:
        """Get all attempts for user on quiz."""
        stmt = select(self.model).where(
            and_(self.model.user_id == user_id, self.model.quiz_id == quiz_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_best_score(self, user_id: int, quiz_id: int) -> int | None:
        """Get best score for user on quiz."""
        stmt = select(func.max(self.model.score)).where(
            and_(self.model.user_id == user_id, self.model.quiz_id == quiz_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or None

    async def get_last_attempt(self, user_id: int, quiz_id: int) -> QuizAttempt | None:
        """Get last attempt for user on quiz."""
        stmt = (
            select(self.model)
            .where(and_(self.model.user_id == user_id, self.model.quiz_id == quiz_id))
            .order_by(desc(self.model.started_at))
            .limit(1)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_attempt_count(self, user_id: int, quiz_id: int) -> int:
        """Get number of attempts for user on quiz."""
        stmt = select(func.count(self.model.id)).where(
            and_(self.model.user_id == user_id, self.model.quiz_id == quiz_id)
        )
        result = await self.db.execute(stmt)
        return result.scalar() or 0
