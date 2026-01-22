"""
API routes for jobfit copilot 
"""
from fastapi import APIRouter 

from .job import router as job_router 
from .resume import router as resume_router
from .projects import router as projects_router 

api_router = APIRouter()

api_router.include_router(job_router)
api_router.include_router(resume_router)
api_router.include_router(projects_router)

__all__ = ["api_router"]

