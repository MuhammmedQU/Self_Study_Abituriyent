"""Student service."""
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import CourseRepository, ModuleRepository, LessonRepository, ResourceRepository, QuizRepository, ProgressRepository
from app.models.course import Course
from app.models.module import Module
from app.models.lesson import Lesson

class StudentService:
    def __init__(self, db: AsyncSession, user_id: int):
        self.db = db
        self.user_id = user_id
        self.course_repo = CourseRepository(db)
        self.module_repo = ModuleRepository(db)
        self.lesson_repo = LessonRepository(db)
        self.resource_repo = ResourceRepository(db)
        self.quiz_repo = QuizRepository(db)
        self.progress_repo = ProgressRepository(db)

    async def get_all_courses(self, skip: int = 0, limit: int = 100):
        return await self.course_repo.get_all_active(skip, limit)

    async def get_course_modules(self, course_id: int, skip: int = 0, limit: int = 100):
        return await self.module_repo.get_by_course(course_id, skip, limit)

    async def get_module_lessons(self, module_id: int, skip: int = 0, limit: int = 100):
        return await self.lesson_repo.get_by_module(module_id, skip, limit)

    async def get_lesson_resources(self, lesson_id: int):
        return await self.resource_repo.get_by_lesson(lesson_id)

    async def get_user_progress(self, module_id: int):
        return await self.progress_repo.get_user_module_progress(self.user_id, module_id)
