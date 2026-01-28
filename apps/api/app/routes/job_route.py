"""
Job ingestion routes.
"""
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.job import Job, JobSource, SeniorityLevel, RoleType
from app.schemas.job import JobCreate, JobDetail, JobSummary, JobProcessingStatus
from app.services.text_cleaner import clean_and_parse_job

router = APIRouter(prefix="/jobs", tags=["jobs"])


# ===================
# Request/Response Models for this endpoint
# ===================

class JobCreateResponse(JobSummary):
    """Response after creating a job."""
    pass


# ===================
# Routes
# ===================

@router.post("", response_model=JobCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_in: JobCreate,
    db: AsyncSession = Depends(get_db),
) -> Job:
    """
    Create a new job from pasted text.
    
    - Cleans HTML and normalizes text
    - Extracts metadata (title, seniority, role type, salary)
    - Parses sections (requirements, nice-to-have, responsibilities)
    - Returns job_id for subsequent analysis
    
    The job is marked as not processed; skill extraction happens asynchronously.
    """
    # Clean and parse the job text
    parsed = clean_and_parse_job(job_in.raw_text, job_in.title)
    
    # Determine title (user provided > extracted > fallback)
    title = job_in.title or parsed["metadata"]["title"] or "Untitled Position"
    
    # Map seniority string to enum
    seniority = None
    if parsed["metadata"]["seniority"]:
        try:
            seniority = SeniorityLevel(parsed["metadata"]["seniority"])
        except ValueError:
            pass
    
    # Map role type string to enum
    role_type = None
    if parsed["metadata"]["role_type"]:
        try:
            role_type = RoleType(parsed["metadata"]["role_type"])
        except ValueError:
            pass
    
    # Determine source
    source = JobSource.URL if job_in.source_url else JobSource.MANUAL
    
    # Create job record
    job = Job(
        title=title,
        company=job_in.company or parsed["metadata"]["company"],
        location=job_in.location or parsed["metadata"]["location"],
        raw_text=job_in.raw_text,
        cleaned_text=parsed["cleaned_text"],
        source=source,
        source_url=job_in.source_url,
        seniority=seniority,
        role_type=role_type,
        remote_type=parsed["metadata"]["remote_type"],
        salary_min=parsed["metadata"]["salary_min"],
        salary_max=parsed["metadata"]["salary_max"],
        salary_currency=parsed["metadata"]["salary_currency"],
        requirements_section=parsed["sections"]["requirements"],
        nice_to_have_section=parsed["sections"]["nice_to_have"],
        responsibilities_section=parsed["sections"]["responsibilities"],
        benefits_section=parsed["sections"]["benefits"],
        is_processed=False,
    )
    
    db.add(job)
    await db.flush()
    await db.refresh(job)
    
    return job


@router.get("/{job_id}", response_model=JobDetail)
async def get_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
) -> Job:
    """
    Get job details by ID.
    
    Returns full job data including extracted sections and skills (if processed).
    """
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found",
        )
    
    return job


@router.get("", response_model=list[JobSummary])
async def list_jobs(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
) -> list[Job]:
    """
    List all jobs with pagination.
    
    Returns job summaries sorted by creation date (newest first).
    """
    result = await db.execute(
        select(Job)
        .order_by(Job.created_at.desc())
        .offset(skip)
        .limit(min(limit, 100))
    )
    return list(result.scalars().all())


@router.get("/{job_id}/status", response_model=JobProcessingStatus)
async def get_job_status(
    job_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Get job processing status.
    
    Returns current status of skill extraction processing.
    """
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found",
        )
    
    status_str = "completed" if job.is_processed else "pending"
    if job.processing_error:
        status_str = "failed"
    
    return {
        "job_id": job.id,
        "status": status_str,
        "is_processed": job.is_processed,
        "error": job.processing_error,
    }


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete a job.
    
    Also removes associated analyses and job_skills (via cascade).
    """
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found",
        )
    
    await db.delete(job)


# ===================
# URL Import
# ===================

from pydantic import BaseModel


class JobImportUrlRequest(BaseModel):
    """Request to import job from URL."""
    url: str
    raw_text: Optional[str] = None  # Optional - will be fetched if not provided
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None


class JobImportUrlResponse(JobSummary):
    """Response after importing job from URL."""
    fetch_method: str  # "provided" | "fetched" | "fallback"
    detected_platform: Optional[str] = None


@router.post("/import-url", response_model=JobImportUrlResponse, status_code=status.HTTP_201_CREATED)
async def import_job_from_url(
    request: JobImportUrlRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Import a job from a URL.
    
    Behavior:
    1. If `raw_text` is provided: Use it directly (user pasted content)
    2. If `raw_text` is missing: Attempt to fetch and parse the URL
    3. If fetch fails (JS-only, blocked): Return helpful fallback message
    
    Supported platforms for direct fetch:
    - Greenhouse (boards.greenhouse.io)
    - Lever (jobs.lever.co)
    - Ashby (jobs.ashbyhq.com)
    - Generic HTML job pages
    
    JS-required platforms (will return fallback):
    - LinkedIn
    - Indeed
    - Glassdoor
    - Workday
    """
    from app.services.url_ingest import url_ingest_service
    
    fetch_method = "provided"
    detected_platform = None
    raw_text = request.raw_text
    
    # If no raw_text provided, attempt to fetch
    if not raw_text:
        result = await url_ingest_service.ingest_url(request.url)
        detected_platform = result.detected_platform
        
        if result.success:
            raw_text = result.raw_text
            fetch_method = "fetched"
        else:
            # Return error with fallback message
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "error": result.error_message or "Could not fetch job description",
                    "fallback_message": result.fallback_message,
                    "requires_js": result.requires_js,
                    "is_blocked": result.is_blocked,
                    "detected_platform": result.detected_platform,
                    "hint": "Please provide the job description text in the 'raw_text' field",
                },
            )
    else:
        fetch_method = "provided"
    
    # Now we have raw_text - create the job
    parsed = clean_and_parse_job(raw_text, request.title)
    
    # Determine title (user provided > extracted > fallback)
    title = request.title or parsed["metadata"]["title"] or "Untitled Position"
    
    # Map seniority string to enum
    seniority = None
    if parsed["metadata"]["seniority"]:
        try:
            seniority = SeniorityLevel(parsed["metadata"]["seniority"])
        except ValueError:
            pass
    
    # Map role type string to enum
    role_type = None
    if parsed["metadata"]["role_type"]:
        try:
            role_type = RoleType(parsed["metadata"]["role_type"])
        except ValueError:
            pass
    
    # Create job record
    job = Job(
        title=title,
        company=request.company or parsed["metadata"]["company"],
        location=request.location or parsed["metadata"]["location"],
        raw_text=raw_text,
        cleaned_text=parsed["cleaned_text"],
        source=JobSource.URL,
        source_url=request.url,
        seniority=seniority,
        role_type=role_type,
        remote_type=parsed["metadata"]["remote_type"],
        salary_min=parsed["metadata"]["salary_min"],
        salary_max=parsed["metadata"]["salary_max"],
        salary_currency=parsed["metadata"]["salary_currency"],
        requirements_section=parsed["sections"]["requirements"],
        nice_to_have_section=parsed["sections"]["nice_to_have"],
        responsibilities_section=parsed["sections"]["responsibilities"],
        benefits_section=parsed["sections"]["benefits"],
        is_processed=False,
    )
    
    db.add(job)
    await db.flush()
    await db.refresh(job)
    
    # Return with extra metadata
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "remote_type": job.remote_type,
        "seniority": job.seniority.value if job.seniority else None,
        "role_type": job.role_type.value if job.role_type else None,
        "source": job.source.value,
        "source_url": job.source_url,
        "is_processed": job.is_processed,
        "summary": job.summary,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
        "fetch_method": fetch_method,
        "detected_platform": detected_platform,
    }