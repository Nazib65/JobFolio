"""
Projects and Github import routes
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import label, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.models.project import Project, ProjectSource
from app.services.github_client import GitHubClient, github_client 
from app.schemas.project import ProjectDetail, ProjectSummary, GitHubSyncResponse

router = APIRouter(prefix="/projects", tags=["projects"])

# ==================
# Request Models
# ==================

class GitHubImportRequest(BaseModel):
    """
    Request to import Github repositories for a user.
    """
    user_id: int 
    repo_urls: list[str] = Field(..., min_length=1, max_length=20)

class ProjectCreateManual(BaseModel):
    """
    Request to create a manual project entry.
    """
    user_id: int 
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    url: Optional[str] = None 
    primary_language: Optional[str] = Field(None, max_length=50)
    topics: list[str] = []

# ==================
# Response Models
# ==================

class ImportResult(BaseModel):
    """
    Result of a single repository import attempt.
    """
    url: str
    success: bool
    project_id: Optional[int] = None
    name: Optional[str] = None
    error: Optional[str] = None 

class GitHubImportResponse(BaseModel):
    """
    Response after github import
    """
    total_requested: int 
    succssful: int 
    failed: int 
    results: list[ImportResult]

class RateLimitInfo(BaseModel):
    """
    GitHub API Rate Limit Information
    """
    limit: int 
    remaining: int 
    reset_at : str 
    authenticated: bool

# ==================
# Routes
# ==================

@router.post("/import", response_model=GitHubImportResponse, status_code=status.HTTP_201_CREATED)
async def import_github_repos(
    request: GitHubImportRequest,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Import GitHub repositories from URLs.
    Skips already imported repositories for the user.
    """
    results=[]
    successful=0
    failed=0

    # Fetch all repos
    repos= await github_client.fetch_multiple_repos(request.repo_urls)

    for i, repo in enumerate(repos):
        url= request.repo_urls[i]

        # Check for errors
        if repo.errors:
            results.append(ImportResult(
                url=url,
                success=False,
                error="; ".join(repo.errors)
            ))
            failed += 1
            continue

        # Check if already imported
        existing = await db.execute(
            select(Project).where(
                Project.user_id == request.user_id,
                Project.github_repo_id == repo.repo_id,
            )
        )
        existing_project = existing.scalar_one_or_none()

        if existing_project:
            # Update existing project 
            existing_project.description = repo.description
            existing_project.primary_language = repo.primary_language
            existing_project.topics = repo.topics
            existing_project.stars_count = repo.stars_count
            existing_project.forks_count = repo.forks_count
            existing_project.languages = repo.languages
            existing_project.readme_content = repo.readme_content
            existing_project.source_updated_at = repo.updated_at
            existing_project.source_pushed_at = repo.pushed_at
            
            results.append(ImportResult(
                url=url, 
                success=True,
                project_id=existing_project.id,
                name=existing_project.name,
                error= "Updated existing project"
            ))
            successful += 1
            continue

        # Create new project
        project= Project(
            user_id=request.user_id,
            source= ProjectSource.GITHUB,
            name= repo.name,
            description= repo.description,
            url=repo.url,
            github_repo_id= repo.repo_id,
            github_full_name= repo.full_name,
            is_fork= repo.is_fork,
            stars_count= repo.stars_count,
            forks_count= repo.forks_count,
            languages= repo.languages,
            primary_language= repo.primary_language,
            readme_content= repo.readme_content,
            topics= repo.topics,
            source_created_at= repo.created_at,
            source_updated_at= repo.updated_at,
            source_pushed_at= repo.pushed_at,
            is_processed=False,
            is_included=True,
        )
        db.add(project)
        await db.flush()

        results.append(ImportResult(
            url=url,
            success=True,
            project_id=project.id,
            name=project.name,
        ))
        successful += 1

    return{
        "total_requested": len(request.repo_urls),
        "successful": successful,
        "failed": failed,
        "results": results,
    }

@router.post("", response_model=ProjectSummary, status_code=status.HTTP_201_CREATED)
async def create_manual_project(
    project_in: ProjectCreateManual,
    db: AsyncSession = Depends(get_db),
) -> Project:
    """
    Create a manual project entry.

    For projects not on Github (Personal projects, work projects, etc.)
    """
    project= Project(
        user_id= project_in.user_id,
        source= ProjectSource.MANUAL,
        name= project_in.name,
        description= project_in.description,
        url= project_in.url,
        primary_language= project_in.primary_language,
        topics= project_in.topics,
        is_processed=True,
        is_included=True,
    )
    db.add(project)
    await db.flush()
    await db.refresh(project)
    
    return project
@router.get("/{project_id}", response_model=ProjectDetail)
async def get_project(
    project_id: int, 
    db: AsyncSession = Depends(get_db),
) -> Project:
    """
    Get project details by ID.
    """
    result= await db.execute(select(Project).where(Project.id==project_id))
    project= result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f" Project {project_id} not found"
        )
    return project

@router.get("", response_model=list[ProjectSummary])
async def list_projects(
    user_id: int, 
    skip: int = 0,
    limit: int =50,
    include_excluded: bool = False,
    db: AsyncSession = Depends(get_db),
) -> list[Project]:
    """
    List all projects for a user with pagination.

    returns project summaries sorted by starts (Github) then creation date.
    """
    query= select(Project).where(Project.user_id== user_id)

    if not include_excluded:
        query= query.where(Project.is_included== True)
    query= query.order_by(
        Project.stars_count.desc().nullslast,
        Project.created_at.desc()
    ).offset(skip).limit(min(limit,100))

    result = await db.execute(query)
    return list(result.scalars().all())

@router.patch("/{project_id}/exclude")
async def exclude_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Exclude a project from analysis.
    
    Useful for hiding forks or irrelevant projects.
    """
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found",
        )
    
    project.is_included = False
    await db.flush()
    
    return {"message": f"Project {project_id} excluded from analysis"}


@router.patch("/{project_id}/include")
async def include_projects(
    project_id: int,
    db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Include a previously excluded project in analysis
    """
    result= await db.execute(select(Project).where(Project.id==project_id))
    project= result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found."
        )
    
    project.is_included= True
    await db.flush()
    
    return { "message": f"Project {project_id} included in analysis." }

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int, 
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete a project by ID.
    """
    result= await db.execute(select(Project).where(Project.id == project_id))
    project= result.scalar_one_or_none()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found."
        )

    await db.delete(project)

@router.get("/github/rate-limit", response_model=RateLimitInfo)
async def check_github_rate_limit() -> dict:
    """
    Check current GitHub API rate limit status.

    Useful for mooniroting API usage before bull imports
    """
    info= await github_client.check_rate_limit()

    if "error" in info:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=info["error"],
        )
    return {
        "limit": info["limit"],
        "remaining": info["remaining"],
        "reset_at": info["reset_at"],
        "authenticated": info["authenticated"],
    }

@router.post("/github/refresh/{project_id}", response_model=ProjectDetail)
async def refresh_github_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
) -> Project:
    """
    Refresh a GitHub project's data from the API.
    
    Updates stars, languages, README, etc.
    """
    result = await db.execute(select(Project).where(Project.id == project_id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project {project_id} not found",
        )
    
    if project.source != ProjectSource.GITHUB:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only refresh GitHub projects",
        )
    
    if not project.github_full_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Project missing GitHub full name",
        )
    
    # Parse owner/repo from full name
    parts = project.github_full_name.split('/')
    if len(parts) != 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid GitHub full name format",
        )
    
    owner, repo = parts
    
    # Fetch fresh data
    repo_data = await github_client.fetch_repo(owner, repo)
    
    if repo_data.errors:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"GitHub API error: {'; '.join(repo_data.errors)}",
        )
    
    # Update project
    project.description = repo_data.description
    project.stars_count = repo_data.stars_count
    project.forks_count = repo_data.forks_count
    project.languages = repo_data.languages
    project.primary_language = repo_data.primary_language
    project.readme_content = repo_data.readme_content
    project.topics = repo_data.topics
    project.source_updated_at = repo_data.updated_at
    project.source_pushed_at = repo_data.pushed_at
    
    await db.flush()
    await db.refresh(project)
    
    return project