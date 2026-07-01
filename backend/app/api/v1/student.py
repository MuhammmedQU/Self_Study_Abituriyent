"""Student endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies import get_current_user
from app.services.student_service import StudentService
from app.services.quiz_service import QuizService
from app.services.progress_service import ProgressService
from pydantic import BaseModel

router = APIRouter(prefix="/student", tags=["student"])

class QuizSubmit(BaseModel):
    quiz_id: int
    score: int
    duration: int
    module_id: int

@router.get("/courses")
async def get_courses(skip: int = 0, limit: int = 100, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = StudentService(db, user["user_id"])
    courses = await service.get_all_courses(skip, limit)
    return {"success": True, "data": [{"id": c.id, "title": c.title, "description": c.description} for c in courses]}

@router.get("/courses/{course_id}/modules")
async def get_modules(course_id: int, skip: int = 0, limit: int = 100, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = StudentService(db, user["user_id"])
    modules = await service.get_course_modules(course_id, skip, limit)
    return {"success": True, "data": [{"id": m.id, "title": m.title} for m in modules]}

@router.get("/modules/{module_id}/lessons")
async def get_lessons(module_id: int, skip: int = 0, limit: int = 100, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = StudentService(db, user["user_id"])
    lessons = await service.get_module_lessons(module_id, skip, limit)
    return {"success": True, "data": [{"id": l.id, "title": l.title} for l in lessons]}

@router.get("/lessons/{lesson_id}/resources")
async def get_resources(lesson_id: int, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = StudentService(db, user["user_id"])
    resources = await service.get_lesson_resources(lesson_id)
    return {"success": True, "data": [{"id": r.id, "title": r.title, "type": r.resource_type, "url": r.url_or_path} for r in resources]}

@router.get("/quiz/{quiz_id}/questions")
async def get_quiz_questions(quiz_id: int, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = QuizService(db, user["user_id"])
    questions = await service.get_random_questions(quiz_id, 10)
    return {"success": True, "data": [{"id": q.id, "text": q.question_text, "options": [{"id": o.id, "text": o.option_text} for o in q.options]} for q in questions]}

@router.post("/quiz/submit")
async def submit_quiz(payload: QuizSubmit, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    quiz_service = QuizService(db, user["user_id"])
    progress_service = ProgressService(db, user["user_id"])
    result = await quiz_service.submit_quiz_attempt(payload.quiz_id, payload.score, payload.duration, payload.module_id)
    await progress_service.update_progress(payload.module_id)
    return {"success": True, "data": result}

@router.get("/progress/{module_id}")
async def get_progress(module_id: int, user: dict = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = ProgressService(db, user["user_id"])
    progress = await service.get_user_all_progress()
    return {"success": True, "data": [{"module_id": p.module_id, "completed": p.completed_lessons} for p in progress]}
