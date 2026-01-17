from enum import Enum
from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, Text, JSON, Enum as SQLEnum, Index 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .user import User 
    from .job import Job 

class AnalysisStatus(str,Enum):
    PENDING="pending"
    PROCESSING="processing"
    COMPLETED="completed"
    FAILED="failed"

class Analysis(Base):
    """
    Stores the complete fit analysis betwenn a user and a job

    This is the entry point for all analysis related operations.
    """
    __tablename__="analysis"

    # Foreign Keys
    user_id: Mapped[int]=mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False, Index=True
    )
    job_id: Mapped[int]=mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"), 
        nullable=False, Index=True
    )
    # Resume used for this analysis (may change over time)
    resume_id: Mapped[Optional[int]]=mapped_column(
        ForeignKey("resumes.id", ondelete="SET NULL"),
        nullable=True
    )

    # Processing Status
    status: Mapped[AnalysisStatus]=mapped_column(
        SQLEnum(AnalysisStatus, name="analysis_status_enum"),
        default=AnalysisStatus.PENDING,
        nullable=False
    )
    processing_error: Mapped[Optional[str]]=mapped_column(Text, nullable=True)
    processing_time_ms= Mapped[Optional[int]]=mapped_column(nullable=True)

    # Scores (0-100 scale)

    #overall fit score
    overall_score: Mapped[Optional[float]]=mapped_column(nullable=True)

    # Coverage : Whhat % of skills does the user have? 
    coverage_score: Mapped[Optional[float]]=mapped_column(nullable=True)

    # Depth : How strong is the evidence for matched skills?
    depth_score: Mapped[Optional[float]]=mapped_column(nullable=True)

    # Bonus: Extra Relavant skills not in the job description
    bonus_score: Mapped[Optional[float]]=mapped_column(nullable=True)

    # Detailed JSON report
    json_detail: Mapped[Optional[dict]]=mapped_column(JSON, nullable=True)

    # AI-Generated summary
    summary: Mapped[Optional[str]]=mapped_column(Text, nullable=True)

    # Strength/Weaknesses quick list
    top_strengths: Mapped[Optional[list]]=mapped_column(JSON, nullable=True)
    top_gaps: Mapped[Optional[list]]=mapped_column(JSON, nullable=True)

    # Is this the latest analysis for this user-job pair?
    is_latest: Mapped[bool]=mapped_column(default=True, nullable=False)

    # User feedback 
    user_rating: Mapped[Optional[int]]=mapped_column(nullable=True)
    user_feedback: Mapped[Optional[str]]=mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"]=relationship("User", back_populates="analyses")
    job: Mapped["Job"]=relationship("Job", back_populates="analyses")

    # Indexes
    __table_args__=(
        Index("ix_analyses_user_latest", "user_id", "is_latest"),
        Index("ix_analyses_user_job", "user_id", "job_id"),
    )
    def __repr__(self) -> str:
        return f"<Analysis(id={self.id}, user_id={self.user_id}, job_id={self.job_id}, score={self.overall_score})>"
