"""Admin service."""
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import CourseRepository, ModuleRepository, LessonRepository, ResourceRepository, QuizRepository, QuestionRepository, ActivityLogRepository
from app.models.course import Course
from app.models.module import Module
from app.models.lesson import Lesson
from app.models.resource import Resource
from app.models.quiz import Quiz

class AdminService:
    def __init__(self, db: AsyncSession, admin_email: str):
        self.db = db
        self.admin_email = admin_email
        self.course_repo = CourseRepository(db)
        self.module_repo = ModuleRepository(db)
        self.lesson_repo = LessonRepository(db)
        self.resource_repo = ResourceRepository(db)
        self.quiz_repo = QuizRepository(db)
        self.question_repo = QuestionRepository(db)
        self.activity_repo = ActivityLogRepository(db)

    async def create_course(self, title: str, description: str = None, thumbnail_path: str = None) -> Course:
        course = await self.course_repo.create({"title": title, "description": description, "thumbnail_path": thumbnail_path})
        await self.activity_repo.create({"user_id": 1, "action": f"Created Course: {title}", "details": None})
        await self.course_repo.commit()
        return course

    async def update_course(self, course_id: int, **kwargs) -> Course:
        course = await self.course_repo.update(course_id, kwargs)
        await self.activity_repo.create({"user_id": 1, "action": f"Updated Course ID {course_id}", "details": None})
        await self.course_repo.commit()
        return course

    async def delete_course(self, course_id: int) -> bool:
        course = await self.course_repo.soft_delete(course_id)
        if course:
            await self.activity_repo.create({"user_id": 1, "action": f"Deleted Course ID {course_id}", "details": None})
            await self.course_repo.commit()
        return course is not None

    async def create_module(self, course_id: int, title: str, description: str = None, order: int = 0) -> Module:
        module = await self.module_repo.create({"course_id": course_id, "title": title, "description": description, "order": order})
        await self.activity_repo.create({"user_id": 1, "action": f"Created Module: {title}", "details": None})
        await self.module_repo.commit()
        return module

    async def update_module(self, module_id: int, **kwargs) -> Module:
        module = await self.module_repo.update(module_id, kwargs)
        await self.activity_repo.create({"user_id": 1, "action": f"Updated Module ID {module_id}", "details": None})
        await self.module_repo.commit()
        return module

    async def delete_module(self, module_id: int) -> bool:
        module = await self.module_repo.soft_delete(module_id, self.admin_email)
        if module:
            await self.activity_repo.create({"user_id": 1, "action": f"Deleted Module ID {module_id}", "details": None})
            await self.module_repo.commit()
        return module is not None

    async def create_lesson(self, module_id: int, title: str, description: str = None, order: int = 0) -> Lesson:
        lesson = await self.lesson_repo.create({"module_id": module_id, "title": title, "description": description, "order": order})
        await self.activity_repo.create({"user_id": 1, "action": f"Created Lesson: {title}", "details": None})
        await self.lesson_repo.commit()
        return lesson

    async def delete_lesson(self, lesson_id: int) -> bool:
        lesson = await self.lesson_repo.soft_delete(lesson_id, self.admin_email)
        if lesson:
            await self.activity_repo.create({"user_id": 1, "action": f"Deleted Lesson ID {lesson_id}", "details": None})
            await self.lesson_repo.commit()
        return lesson is not None

    async def create_resource(self, lesson_id: int, title: str, resource_type: str, url_or_path: str) -> Resource:
        resource = await self.resource_repo.create({"lesson_id": lesson_id, "title": title, "resource_type": resource_type, "url_or_path": url_or_path})
        await self.activity_repo.create({"user_id": 1, "action": f"Created Resource: {title}", "details": None})
        await self.resource_repo.commit()
        return resource

    async def delete_resource(self, resource_id: int) -> bool:
        resource = await self.resource_repo.soft_delete(resource_id, self.admin_email)
        if resource:
            await self.activity_repo.create({"user_id": 1, "action": f"Deleted Resource ID {resource_id}", "details": None})
            await self.resource_repo.commit()
        return resource is not None

    async def create_quiz(self, lesson_id: int, title: str, passing_score: int = 70) -> Quiz:
        quiz = await self.quiz_repo.create({"lesson_id": lesson_id, "title": title, "passing_score": passing_score})
        await self.activity_repo.create({"user_id": 1, "action": f"Created Quiz: {title}", "details": None})
        await self.quiz_repo.commit()
        return quiz
