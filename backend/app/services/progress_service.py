"""Progress service."""
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import ProgressRepository, LessonRepository, QuizAttemptRepository, ModuleRepository

class ProgressService:
    def __init__(self, db: AsyncSession, user_id: int):
        self.db = db
        self.user_id = user_id
        self.progress_repo = ProgressRepository(db)
        self.lesson_repo = LessonRepository(db)
        self.quiz_repo = QuizAttemptRepository(db)
        self.module_repo = ModuleRepository(db)

    async def update_progress(self, module_id: int, current_lesson_id: int = None, time_spent: int = 0):
        progress = await self.progress_repo.get_user_module_progress(self.user_id, module_id)
        if not progress:
            progress = await self.progress_repo.create_or_update(
                self.user_id, module_id,
                {"current_lesson_id": current_lesson_id, "total_time_spent": time_spent}
            )
        else:
            progress.current_lesson_id = current_lesson_id
            progress.total_time_spent = (progress.total_time_spent or 0) + time_spent
            progress.last_activity = datetime.utcnow()
            progress.updated_at = datetime.utcnow()
            self.db.add(progress)
            await self.db.flush()
        await self.progress_repo.commit()
        return progress

    async def calculate_completion_percentage(self, module_id: int) -> float:
        progress = await self.progress_repo.get_user_module_progress(self.user_id, module_id)
        if not progress:
            return 0.0
        module = await self.module_repo.get(module_id)
        if not module or not module.lessons:
            return 0.0
        total_lessons = len(module.lessons)
        completed = progress.completed_lessons or 0
        return (completed / total_lessons * 100) if total_lessons > 0 else 0.0

    async def mark_lesson_completed(self, module_id: int, lesson_id: int):
        progress = await self.progress_repo.get_user_module_progress(self.user_id, module_id)
        if progress:
            if progress.completed_lessons is None:
                progress.completed_lessons = 0
            progress.completed_lessons += 1
            progress.updated_at = datetime.utcnow()
            self.db.add(progress)
            await self.db.flush()
        await self.progress_repo.commit()

    async def get_user_all_progress(self):
        return await self.progress_repo.get_user_all_progress(self.user_id)
