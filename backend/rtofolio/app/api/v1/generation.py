from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel
from app.ai.pipelines.portfolio_pipeline import generate_portfolio_pipeline

router = APIRouter(prefix="/generation", tags=["generation"])

class GenerationRequest(BaseModel):
    resume_markdown: str

@router.post("/")
async def generate_portfolio(request: GenerationRequest):
    return generate_portfolio_pipeline(request.resume_markdown)