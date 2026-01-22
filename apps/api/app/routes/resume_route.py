"""
Resume upload and text extraction routes.
"""
import hashlib
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form,  status
from sqlalchemy import label, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_db
from app.models.resume import Resume
from app.services.pdf_extract import PDFExtractor, ResumeParser

router= APIRouter(prefix="/resumes", tags=["resumes"])
settings= get_settings()

#==================
# Response Models
# =================

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ResumeUploadResponse(BaseModel):
    """
    Response after uploading a resume.
    """
    user_id: int 
    file_name: str
    file_size_bytes: int 
    page_count: int 
    line_count: int 
    bullent_count: int 
    is_processed: bool
    created_at: datetime

    class config:
        from_attributes = True

class ResumeDetailResponse(ResumeUploadResponse):
    """
    Full resume details
    """
    raw_text: Optional[str] = None 
    bullet_points: Optional[list[dict]] = None
    parsed_json: Optional[dict] = None 
    processing_error: Optional[str] = None 
    is_active: bool

class ResumeListItem(BaseModel):
    """
    Resume summary for listings
    """
    id: int 
    user_id: int 
    file_name: str 
    label: Optional[str]
    is_active: bool 
    is_processed: bool
    created_at: datetime 

    class config:
        from_attributes = True

# ==================
# Routes
# ==================
@router.post("", response_model=ResumeUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    user_id: int = Form(...),
    label: Optional[str] = Form(None),
    set_active: bool = Form(True),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Upload a resume PDF

    - Extracts text using pdfplumber
    - Segments into lines and bullet points
    - Stores raw text and structured data
    - Optionally sets as active resume for the user
    
    Returns resume_id for subsequent analysis.
    """""
    # Validate file type 
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided."
        )
    
    allowed_types = ['.pdf']
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_types: 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        )
    # Read file content 
    content= await file.read()
    file_size = len(content)

    # Validate file size
    max_size = settings.max_upload_size_mb * 1024 * 1024
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds the maximum limit of {settings.max_upload_size_mb} MB."
        )
    
    # Gnerate unique filename for storage
    file_hash = hashlib.sha256(content).hexdigest()
    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    file_path= settings.upload_dir / unique_name 

    # Save file to disk
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'wb') as f:
        f.write(content)
    
    # Extract text from pdf
    try:
        extracted = await PDFExtractor.extract_from_bytes(content, file.filename)
    except Exception as e:
        # Clean up file on extraction failure 
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Failed to extract text from PDF: {str(e)}"
        )
    if not extracted.raw_text and not extracted.errors:
        extracted.errors.append("No text could be extracted from PDF.")

    # Parse basic structure 
    parsed_structure = ResumeParser.parse_basic_structure(extracted.lines)

    # If setting as activate, deatcivate other resumes for this user 
    if set_active:
        await db.execute(
            update(Resume)
            .where(Resume.user_id == user_id)
            .values(is_active=False)
        )
    # Create resume record
    resume= Resume(
        user_id=user_id,
        file_path=str(file_path),
        file_name=file.filename,
        file_size_bytes=file_size,
        file_hash=file_hash,
        mime_type=file.content_type or "application/pdf",
        raw_text=extracted.raw_text,
        bullet_points=extracted.bullet_points,
        parsed_json={
            "page_count": extracted.page_count,
            "line_count": len(extracted.lines),
            "lines": extracted.lines,
            "sections": parsed_structure["sections"],
            "contact_hints": parsed_structure["contact_hints"],
            "skills_raw": parsed_structure["skills_raw"],
        },
        label=label,
        is_active=set_active,
        is_processed=True,
        processing_error="; ".join(extracted.errors) if extracted.errors else None,

    )
    db.add(resume)
    await db.flush()
    await db.refresh(resume)

    return {
        "id": resume.id,
        "user_id": resume.user_id,
        "file_name": resume.file_name,
        "fime_size_bytes": resume.file_size_bytes,
        "page_count": extracted.page_count,
        "line_count": len(extracted.lines),
        "bullent_count": len(extracted.bullet_points),
        "is_processed": resume.is_processed,
        "created_at": resume.created_at,
    }
@router.get("/{resume_id}", response_model=ResumeDetailResponse)
async def get_resume(
    resume_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Get resume details by ID

    Returns full resume data including extracted text and structure
    """
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume= result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found."
        )
    parsed = resume.parsed_json or {}
    return {
        "id" : resume.id,
        "user_id": resume.user_id,
        "file_name": resume.file_name,
        "file_size__bytes": resume.file_size_bytes,
        "page_count": parsed.get("page_count", 0),
        "line_count": parsed.get("line_count", 0),
        "bullet_count": len(resume.bullet_points or []),
        "is_processed": resume.is_processed,
        "raw_text": resume.raw_text,
        "bullet_points": resume.bullet_points,
        "parsed_json": resume.parsed_json,
        "processing_error": resume.processing_error,
        "is_active": resume.is_active,
        "label": resume.label, 
    }
@router.get("", response_model=list[ResumeListItem])
async def list_resumes(
    user_id: int, 
    skip: int =0, 
    limit :int =20,
    db: AsyncSession = Depends(get_db),
) -> list[Resume]:
    """
    List Resume for a user.

    Returns resume summarie sorted by creation date(newest first).
    """

    result= await db.execute(
        select(Resume)
        .where(Resume.user_id==user_id)
        .order_by(Resume.created_at.desc())
        .offset(skip)
        .limit(min(limit, 100))
    )
    return list(result.scalars().all())

@router.patch("/{resume_id}/activate", response_model=ResumeListItem)
async def set_active_resume(
    resume_id: int,
    db: AsyncSession = Depends(get_db), 
) -> Resume:
    """
    Set a resume as the active resume for the user.

    Deactivates other resumes for the same user.
    """
    result= await db.exevute(select(Resume).where(Resume.id==resume_id))
    resume= result.sscalr_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found."
        )
    
    # Deactivate other resumes for the user
    await db.execute(
        update(Resume)
        .where(Resume.user_id==resume.user_id, Resume.id != resume_id)
        .values(is_active=False)
    )
    resume.is_active = True
    await db.flush()
    await db.refresh(resume)
    
    return resume

@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: int, 
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete a resume by ID.

    Also removes the file from disk.
    """
    result= await db.execute(select(Resume).where(Resume.id == resume_id))
    resume= result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found."
        )
    
    # Delete the file from storage
    file_path= Path(resume.file_path)
    if file_path.exists():
        file_path.unlink()
    
    await db.delete(resume)

@router.get("/{resume_id}/bullets", response_model=list[dict])
async def get_resume_bullets(
    resume_id: int, 
    db: AsyncSession = Depends(get_db),

) -> list[dict]:
    """
    Get bullet points from a resume by ID

    Returns list of bullet points with context for skill matching.
    """
    result= await db.execute(select(Resume).where(Resume.id == resume_id))
    resume= result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found."
        )
    return resume.bullet_points or []
