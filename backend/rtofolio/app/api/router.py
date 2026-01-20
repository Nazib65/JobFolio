from fastapi import APIRouter
from app.api.v1 import portfolio, resume_parse, generation

api_router = APIRouter()
api_router.include_router(portfolio.router, prefix="/v1")
api_router.include_router(resume_parse.router, prefix="/v1")
api_router.include_router(generation.router, prefix="/v1")