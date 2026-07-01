"""Quiz service."""
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import QuizRepository, QuestionRepository, QuizAttemptRepository, ProgressRepository, LessonRepository

class QuizService:
    def __init__(self, db: AsyncSession, user_id: int):
        self.db = db
        self.user_id = user_id
        self.quiz_repo = QuizRepository(db)
        self.question_repo = QuestionRepository(db)
        self.attempt_repo = QuizAttemptRepository(db)
        self.progress_repo = ProgressRepository(db)
        self.lesson_repo = LessonRepository(db)

    async def get_quiz(self, quiz_id: int):
        return await self.quiz_repo.get(quiz_id)

    async def get_random_questions(self, quiz_id: int, count: int = 10):
        total = await self.question_repo.count_by_quiz(quiz_id)
        if total < count:
            count = total
        return await self.question_repo.get_random_questions(quiz_id, count)

    async def submit_quiz_attempt(self, quiz_id: int, score: int, duration: int, module_id: int) -> dict:
        attempt_count = await self.attempt_repo.get_attempt_count(self.user_id, quiz_id)
        attempt = await self.attempt_repo.create({
            "user_id": self.user_id,
            "quiz_id": quiz_id,
            "attempt_number": attempt_count + 1,
            "score": score,
            "finished_at": datetime.utcnow(),
            "duration": duration,
        })
        await self.attempt_repo.commit()

        quiz = await self.quiz_repo.get(quiz_id)
        passed = score >= quiz.passing_score

        return {
            "attempt_id": attempt.id,
            "score": score,
            "passed": passed,
            "passing_score": quiz.passing_score,
        }

    async def get_best_score(self, quiz_id: int):
        return await self.attempt_repo.get_best_score(self.user_id, quiz_id) or 0

    async def get_last_score(self, quiz_id: int):
        last = await self.attempt_repo.get_last_attempt(self.user_id, quiz_id)
        return last.score if last else None
