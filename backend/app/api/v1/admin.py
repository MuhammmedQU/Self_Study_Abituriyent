"""Admin endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.dependencies import require_admin
from app.services.admin_service import AdminService
from app.models.course import Course
from app.models.module import Module
from app.models.lesson import Lesson
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["admin"])

class CourseCreate(BaseModel):
    title: str
    description: str = None
    thumbnail_path: str = None

class ModuleCreate(BaseModel):
    course_id: int
    title: str
    description: str = None
    order: int = 0

class LessonCreate(BaseModel):
    module_id: int
    title: str
    description: str = None
    order: int = 0

class ResourceCreate(BaseModel):
    lesson_id: int
    title: str
    resource_type: str
    url_or_path: str

class QuizCreate(BaseModel):
    lesson_id: int
    title: str
    passing_score: int = 70

@router.post("/courses")
async def create_course(payload: CourseCreate, user: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    service = AdminService(db, user["email"])
    course = await service.create_course(payload.title, payload.description, payload.thumbnail_path)
    return {"success": True, "data": {"id": course.id, "title": course.title}}

@router.get("/courses")
async def get_courses(skip: int = 0, limit: int = 100, user: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    service = AdminService(db, user["email"])
    courses = await service.course_repo.get_all_active(skip, limit)
    return {"success": True, "data": [{"id": c.id, "title": c.title} for c in courses]}

@router.post("/modules")
async def create_module(payload: ModuleCreate, user: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    service = AdminService(db, user["email"])
    module = await service.create_module(payload.course_id, payload.title, payload.description, payload.order)
    return {"success": True, "data": {"id": module.id, "title": module.title}}

@router.get("/modules/{course_id}")
async def get_modules(course_id: int, skip: int = 0, limit: int = 100, user: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    service = AdminService(db, user["email"])
    modules = await service.module_repo.get_by_course(course_id, skip, limit)
    return {"success": True, "data": [{"id": m.id, "title": m.title} for m in modules]}

@router.post("/lessons")
async def create_lesson(payload: LessonCreate, user: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    service = AdminService(db, user["email"])
    lesson = await service.create_lesson(payload.module_id, payload.title, payload.description, payload.order)
    return {"success": True, "data": {"id": lesson.id, "title": lesson.title}}

@router.delete("/courses/{course_id}")
async def delete_course(course_id: int, user: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    service = AdminService(db, user["email"])
    result = await service.delete_course(course_id)
    if not result:
        raise HTTPException(status_code=404, detail="Course not found")
    return {"success": True, "message": "Course deleted"}

@router.delete("/modules/{module_id}")
async def delete_module(module_id: int, user: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    service = AdminService(db, user["email"])
    result = await service.delete_module(module_id)
    if not result:
        raise HTTPException(status_code=404, detail="Module not found")
    return {"success": True, "message": "Module deleted"}

@router.delete("/lessons/{lesson_id}")
async def delete_lesson(lesson_id: int, user: dict = Depends(require_admin), db: AsyncSession = Depends(get_db)):
    service = AdminService(db, user["email"])
    result = await service.delete_lesson(lesson_id)
    if not result:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {"success": True, "message": "Lesson deleted"}
