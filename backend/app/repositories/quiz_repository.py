"""Quiz repository."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.quiz import Quiz
from app.repositories.base import BaseRepository


class QuizRepository(BaseRepository[Quiz]):
    """Quiz repository."""

    def __init__(self, db: AsyncSession):
        super().__init__(db, Quiz)

    async def get_by_lesson(self, lesson_id: int) -> Quiz | None:
        """Get quiz for a lesson."""
        stmt = select(self.model).where(
            self.model.lesson_id == lesson_id, self.model.deleted_at.is_(None)
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_with_questions(self, quiz_id: int) -> Quiz | None:
        """Get quiz with questions and options."""
        stmt = (
            select(self.model)
            .where(self.model.id == quiz_id, self.model.deleted_at.is_(None))
            .options(selectinload(self.model.questions))
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def soft_delete(self, quiz_id: int, deleted_by: str) -> Quiz | None:
        """Soft delete quiz."""
        quiz = await self.get(quiz_id)
        if not quiz:
            return None
        quiz.deleted_at = datetime.utcnow()
        quiz.deleted_by = deleted_by
        self.db.add(quiz)
        await self.db.flush()
        return quiz
