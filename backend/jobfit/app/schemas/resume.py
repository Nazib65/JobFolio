""" 
Resume-related pydantic schemas
"""
from datetime import datetime 
from typing import Optional, Any 

from pydantic import BaseModel, Field
from .base import BaseSchema, IDMixin, TimestampMixin

# ===================
# Parsed Resume Structure
# ===================
class ContactInfo(BaseModel):
    """ Parse Contact information"""
    name: Optional[str]=None
    email: Optional[str]=None 
    phone: Optional[str]=None
    linkedin: Optional[str]=None
    gtihub: Optional[str]=None
    website: Optional[str]=None
    location: Optional[str]=None

class ExperienceItem(BaseModel):
    """ Parse work experience item """
    comapany: str
    title: str
    location: Optional[str]=None 
    start_date: Optional[datetime]=None 
    end_date: Optional[datetime]=None 
    is_current: Optional[bool]=False
    bullets: Optional[list[str]]=[]
    technologies: Optional[list[str]]=[]

class EducationItem(BaseModel):
    """ Parse education item"""
    instituition: str
    degree: str 
    location: Optional[str]=None
    start_date: Optional[datetime]=None
    end_date: Optional[datetime]=None
    is_current: Optional[bool]=False
    bullets: Optional[list[str]]=[]
    technologies: Optional[list[str]]=[]

class CertificationItem(BaseModel):
    """ Parse certification item"""
    name: str
    issuer: Optional[str]=None
    date: Optional[datetime]=None
    expiry: Optional[datetime]=None
    credential_id: Optional[str]=None

class ProjectItem(BaseModel):
    """ Parse Project Item """
    name: str 
    description: Optional[str]=None
    url: Optional[str]=None
    technologies: Optional[list[str]]=[]
    dates: Optional[str]=None

class ParsedResume(BaseModel):
    """ Complete parsed resume structure"""
    contact: ContactInfo = ContactInfo()
    summary: Optional[str]=None
    skills_section: Optional[list[str]]=[]
    education: list[EducationItem]=[]
    experience: list[ExperienceItem]=[]
    projects: list[ProjectItem]=[]
    certifications: list[CertificationItem]=[]
    languages: Optional[list[str]]=[]
    interests: Optional[list[str]]=[]


# ===================
# Request Schemas
# ===================

class ResumeUploadRequest(BaseModel):
    """ Metada for resume upload"""
    label: Optional[str]=Field(None, max_length=100)
    set_as_active: bool=True

class ResumeUpdate(BaseModel):
    """ Schema for updating resume metadata"""
    label: Optional[str]=Field(None, max_length=100)
    is_active: Optional[bool]=None

# ===================
# Response Schemas
# ===================

class ResumeBase(BaseSchema, IDMixin):
    """Base Resume Response """
    file_name: str
    label: Optional[str]=None
    is_active: bool
    is_processed: bool

class ResumeSummary(ResumeBase, TimestampMixin):
    """ Resume summary for listings """
    file_size_bytes: Optional[int]=None

class ResumeDetail(ResumeBase, TimestampMixin):
    """ Detailed Resume Response """
    file_size_bytes: Optional[int]=None
    mime_type: Optional[str]=None
    processing_error: Optional[str]=None

    parsed_json: Optional[ParsedResume]=None

    # Skills extracted
    skills_count: int = 0

class ResumeUploadResponse(BaseModel):
    """ Response after uploading a resume """
    resume_id: int
    file_name: str
    status: str
    message: str

class ResumeProcessingStatus(BaseModel):
    """ Resume processing status """
    resume_id: int 
    status: str 
    is_processed: bool 
    error: Optional[str]=None
    skills_extracted: Optional[int]=None 

class BulletPoint(BaseModel):
    """ Bullet point schema for resume sections """
    text: str
    context: str
    source_section: str
    embedding_id: Optional[str]=None 
