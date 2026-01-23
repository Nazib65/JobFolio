""" 
Project related Pydantic Schemas 
"""

from datetime import datetime 
from typing import Optional 
from pydantic import BaseModel, Field, HttpUrl
from .base import BaseSchema, IDMixin, TimestampMixin

# ===================
# Request Schemas
# ===================

class ProjectCreate(BaseModel):
    """ Schema for manually creating a project """
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    url: Optional[HttpUrl] = None
    primary_language: Optional[str] = Field(None, max_length=50)
    topics: list[str] = []

class ProjectUpdate(BaseModel):
    """ Schema for updating a project """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=5000)
    url: Optional[HttpUrl] = None 
    is_included: Optional[bool] = None 
    topics: Optional[list[str]] = None 

class GitHubSyncRequest(BaseModel):
    """ Request to sync Github repositories """
    include_forks: bool = False
    min_stars: int = 0
    languages_filter: Optional[list[str]] = None 
    max_repos: int = 50

# ===================
# Response Schemas
# ===================

class ProjectBase(BaseSchema, IDMixin):
    """ Base project response """
    name: str 
    description: Optional[str] = None 
    url: Optional[str] = None 
    source: str #github, manual
    primary_language: Optional[str] = None 
    is_included: bool = True 

class ProjectSummary(ProjectBase, TimestampMixin):
    """ Project summary for listings """
    languages: Optional[dict[str, int]] = None 
    topics: list[str] = []
    stars_count: Optional[int] = None 

class ProjectDetail(ProjectBase, TimestampMixin):
    """ Full peoject detail """
    languages: Optional[dict[str, int]] = None 
    topics: list[str] = []
    readme_summary: Optional[str] = None 

    # Github specific
    github_full_name: Optional[str] = None 
    is_fork: Optional[bool] = None 
    stars_count: Optional[int] = None 
    forks_count: Optional[int] = None 
    source_created_at: Optional[datetime] = None 
    source_updated_at: Optional[datetime] = None 

    # Processing
    is_processed: bool
    processing_error: Optional[str] = None 

class GitHubSyncResponse(BaseModel):
    """ Response after github sync """
    repos_found: int
    repos_imported: int
    repos_updated: int 
    repos_skipped: int 
    errors: list[str] = []

class GitHubRepoPreview(BaseModel):
    """ Preview of a Github repo for selection """
    github_repo_id: int 
    full_name: str
    description: Optional[str]
    primary_language: Optional[str]
    stars_count: int 
    is_fork: bool
    updated_at: datetime 
    alread_imported: bool


