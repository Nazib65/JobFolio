"""
JobSkill Model linking Jobs to Skills with proficiency levels
"""
from typing import TYPE_CHECKING, Optional
from enum import Enum

from sqlalchemy import ForeignKey, String, Text, Enum as SQLEnum, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base 

if TYPE_CHECKING:
    from .job import Job
    from .skill import Skill

class SkillImportance(str, Enum):
    """
    How important/required is this skill for the job.
    Used for weighting in scoring.
    """
    NICE_TO_HAVE=1
    PREFERRED=2
    REQUIRED=3

class JobSkill(Base):
    """
    Links a job posting to a required skil with metadata

    Tracks:
    - How important the skill is for the job
    - Where it was mentioned (description, requirements, benefits, etc)
    - Confidence of extraction
    """
    __tablename__="job_skills"

    # ForeignKey
    jpb_id: Mapped[int]=mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False, 
        index=True
    )
    skill_id: Mapped[int]=mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Importance Level
    importance: Mapped[SkillImportance]=mapped_column(
        SQLEnum(SkillImportance, name="skill_importance"),
        default=SkillImportance.REQUIRED,
        nullable=False
    )
    # Confidence for extraction (0.0 - 1.0)
    confidence: Mapped[float]=mapped_column(default=1.0, nullable=False)

    # Raw text where skill was found 
    source_text=Mapped[Optional[str]]=mapped_column(Text, nullable=True)

    # Which section of the JD
    source_section: Mapped[Optional[str]]=mapped_column(String(50), nullable=True)

    # Number of times mentioned
    mention_count: Mapped[int]=mapped_column(default=1, nullable=False)

    # Years of experience required 
    years_required: Mapped[Optional[int]]=mapped_column(nullable=True)

    # Realtionships 
    job: Mapped["Job"]=relationship("Job", back_populates="skills")
    skill: Mapped["Skill"]=relationship("Skill", back_populates="job_skills")

    # Constraints 
    __table_args__=(
        UniqueConstraint("job_id", "skill_id", name="uq_job_skill"),
        Index("ix_job_skills_job_importance", "job_id", "importance"),
    )

    def __repr__(self) -> str:
        return f"<JobSkill(job_id={self.job_id}, skill_id={self.skill_id}, importance={self.importance.name})>"
    