"""
Job Model for job descriptions being analyzed
"""
from enum import Enum
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .job_skill import JobSkill
    from .analysis import Analysis

class SeniorityLevel(str, Enum):
    """
    Job Seniority Levels
    """
    INTERN="intern"
    JUNIOR="junior"
    MID="mid"
    SENIOR="senior"
    LEAD="lead"
    MANAGER="manager"
    DIRECTOR="director"
    VP="vp"
    EXECUTIVE="executive"

class RoleType(str, Enum):
    """
    Primary role type clasifications
    """
    BACKEND="backend"
    FRONTEND="frontend"
    FULLSTACK="fullstack"
    DEVOPS="devops"
    DATA_ENGINEER="data_engineer"
    DATA_SCIENTIST="data_scientist"
    ML_ENGINEER="ml_engineer"
    PRODUCT_MANAGER="product_manager"
    DESIGNER="designer" 
    QA="qa"
    MOBILE="mobile"
    EMBEDDED="embedded"
    PLATFORM="platform"
    SECURITY="security"
    CYBERSECURITY="cybersecurity"
    SYSTEMS_ADMIN="systems_admin"
    SALESFORCE_ADMIN="salesforce_admin"
    PROJECT_MANAGER="project_manager"
    BUSINESS_ANALYST="business_analyst"
    PRODUCT_MANAGER="product_manager"
    DATA_ANALYST="data_analyst"
    AI_ENGINEER="ai_engineer"
    GAME_DEVELOPER="game_developer"
    UX_UI_DESIGNER="ux_ui_designer"
    BLOCKCHAIN_DEVELOPER="blockchain_developer"
    MLOPS="mlops"
    OTHER="other"

class JobSource(str, Enum):
    """
    Source of the job description
    """
    MANUAL="manual"
    URL="url"   
    GREENHOUSE="greenhouse"
    LINKEDIN="linkedin"
    INDEED="indeed"
    GLASSDOOR="glassdoor"
    MONSTER="monster"
    COMPANY_WEBSITE="company_website"
    REFERRAL="referral"
    LEVER="lever"
    WORKDAY="workday"
    OTHER_ATS="other_ats"

class Job(Base):
    """
    Represents a job posting being analyzed.
    Jobs can be:
    - Pasted directly as text
    - Imported from a URL
    -Fetched via jod board APIs

    """
    __tablename__="jobs"

    # Core Info
    title: Mapped[str]=mapped_column(String(255), nullable=False)
    company: Mapped[Optional[str]]=mapped_column(String(255), nullable=True, index=True)
    location: Mapped[Optional[str]]=mapped_column(String(255), nullable=True)
    description: Mapped[Text]=mapped_column(Text, nullable=False)
    remote_type: Mapped[Optional[str]]=mapped_column(String(55), nullable=True)

    # Classifications
    seniority: Mapped[Optional[SeniorityLevel]]=mapped_column(
        SQLEnum(SeniorityLevel, name="seniority_level"),
        nullable=True
    )
    role_type: Mapped[Optional[RoleType]]=mapped_column(
        SQLEnum(RoleType, name="role_type"),
        nullable=True
    )
    # Content
    raw_text: Mapped[str]=mapped_column(Text, nullable=False)
    cleaned_text: Mapped[Optional[str]]=mapped_column(Text, nullable=True)

    # Extracted Sections
    requirement_section: Mapped[Optional[str]]=mapped_column(Text, nullable=True)
    nice_to_have_section: Mapped[Optional[str]]=mapped_column(Text, nullable=True)
    responsibilities_section: Mapped[Optional[str]]=mapped_column(Text, nullable=True)
    benefits_section: Mapped[Optional[str]]=mapped_column(Text, nullable=True)

    # Compensation Info
    salary_min: Mapped[Optional[int]]=mapped_column(nullable=True)
    salary_max: Mapped[Optional[int]]=mapped_column(nullable=True)
    salary_currency: Mapped[Optional[str]]=mapped_column(String(10), nullable=True)

    # Source Tracking 
    source: Mapped[JobSource]=mapped_column(
        SQLEnum(JobSource, name="job_source"),
        default=JobSource.MANUAL,
        nullable=False
    )
    source_url: Mapped[Optional[str]]=mapped_column(String(1000), nullable=True)
    external_id: Mapped[Optional[str]]=mapped_column(String(255), nullable=True)

    # Processing Status
    is_processed: Mapped[bool]=mapped_column(nullable=False, default=False)
    processing_error: Mapped[Optional[str]]=mapped_column(Text, nullable=True)

    # AI Summary
    ai_summary: Mapped[Optional[str]]=mapped_column(Text, nullable=False)

    # Relationships 
    skills: Mapped[list["JobSkill"]]=relationship(
        "JobSkill",
        back_populates="job",
        cascade="all, delete-orphan"
    )
    analyses: Mapped[list["Analysis"]]=relationship(
        "Analysis",
        back_populates="job",
        cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"<Job.id={self.id}, title={self.title}, company={self.company}>"


