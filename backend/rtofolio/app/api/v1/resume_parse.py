import os
import tempfile

from fastapi import APIRouter, File, HTTPException, UploadFile, Depends
from app.services.resume_parser import parsePDF
from app.utils.auth_middleware import get_current_user

router = APIRouter(prefix="/resume" , tags = ["resume"])

@router.post("/")
async def parse_resume(resume: UploadFile = File(...), user = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if resume.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_path = temp_file.name
            temp_file.write(await resume.read())

        markdown = parsePDF(temp_path)
        return {"markdown": markdown}
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)