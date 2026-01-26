"""
Job related pydantic schemas
"""
from typing import Optional 
from pydantic import BaseModel, Field, HttpUrl
from .base import BaseSchema, IDMixin, TimestampMixin

# ===================
# Request Schemas
# ===================
class JobCreate(BaseModel):
    """ Schema for creating a job  from pasted text """
    raw_text: str = Field(..., min_length=50, max_length=50000)
    title: Optional[str]=Field(None, max_length=255)
    company: Optional[str]=Field(None, max_length=255)
    location: Optional[str]=Field(None, max_length=255)
    source_url: Optional[str]=Field(None, max_length=1000)


class JobImportUrl(BaseModel):
    """" Schema for importing a job from url """
    url: HttpUrl

class JobUpdate(BaseModel):
    """ Schema for updating job details """
    title: Optional[str] = Field(None, max_length=255)
    comapny: Optional[str] = Field(None, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    remote_type: Optional[str] = Field(None, pattern="^(remote|hybrid|onsite)$")


# ===================
# Response Schemas
# ===================
class JobBase(BaseSchema, IDMixin):
    """ Base Job Response Schema """
    title: str
    company: Optional[str] = None
    location: Optional[str]=None 
    remote_type: Optional[str]=None 
    seniority: Optional[str]=None 
    role_type: Optional[str]=None
    source: str
    source_url: Optional[str]=None 


class JobSummary(JobBase, TimestampMixin):
    """ Job Summary for listing """
    is_processed: bool = False
    summary: Optional[str]=None 

class JobSkillItem(BaseModel):
    """ Skill extracted from job """
    skill_id: int 
    skill_name: str 
    category: str 
    importance: str
    confidence: float 
    mention_count: int 
    years_required: Optional[int] = None
    source_text: Optional[str] = None

class JobDetail(JobBase, TimestampMixin):
    """ Full job detail response """
    raw_text: str 
    cleaned_text: Optional[str] = None 
    summary: Optional[str] = None 
    is_processed: bool
    processing_error: Optional[str] = None

    # Salary info 
    min_salary: Optional[float] = None 
    salary_max: Optional[float] = None 
    salary_currency: Optional[str] = None 

    # Extracted sections
    requirement_section: Optional[str] = None 
    nice_to_have_section: Optional[str] = None 
    responsibilities_section: Optional[str] = None

    skills: list[JobSkillItem] = []

class JobProcessingStatus(BaseModel):
    """ Job Processing Status """
    job_id: int 
    status: str
    is_processed: bool
    error: Optional[str] = None 

class JobComparisonItem(BaseModel):
    """ Job Summary for comaprison views """
    job_id: int 
    title: str
    company: Optional[str] 
    overall_score: Optional[float]
    coverage_score: Optional[float]
    top_matches: list[str]
    top_gaps: list[str]



