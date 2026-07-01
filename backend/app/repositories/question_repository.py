"""Question repository."""

from sqlalchemy import and_, select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.question import Question
from app.repositories.base import BaseRepository


class QuestionRepository(BaseRepository[Question]):
    """Question repository."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Question)

    async def get_by_quiz(self, quiz_id: int) -> list[Question]:
        """Get all questions for a quiz."""
        stmt = (
            select(self.model)
            .where(self.model.quiz_id == quiz_id)
            .options(selectinload(self.model.options))
        )
        result = await self.db.execute(stmt)
        return result.scalars().unique().all()

    async def get_random_questions(self, quiz_id: int, count: int = 10) -> list[Question]:
        """Get random questions from quiz."""
        stmt = (
            select(self.model)
            .where(self.model.quiz_id == quiz_id)
            .order_by(func.random())
            .limit(count)
            .options(selectinload(self.model.options))
        )
        result = await self.db.execute(stmt)
        return result.scalars().unique().all()

    async def count_by_quiz(self, quiz_id: int) -> int:
        """Count questions in quiz."""
        stmt = select(func.count(self.model.id)).where(self.model.quiz_id == quiz_id)
        result = await self.db.execute(stmt)
        return result.scalar() or 0
