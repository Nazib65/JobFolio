"""
Project Model for Github repositories and manual project entries
"""
from enum import Enum 
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, Enum as SQLEnum, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base 
if TYPE_CHECKING:
    from .user import User 

class ProjectSource(str, Enum):
    """
    Source of the project
    """
    GITHUB="github"
    GITLAB="gitlab"
    BITBUCKET="bitbucket"
    MANUAL="manual"

class Project(Base):
    """
    Represents a user's project, either linked from a Github repository or manually entered.

    Used to extract skills and provide eveidence for skill claims
    """
    __tablename__="projects"

    # Ownership
    user_id: Mapped[int]=mapped_column(
     ForeignKey("users.id", ondelete="CASCADE"),
     nullable=False,
     index=True   
    )
    # Source
    source: Mapped[ProjectSource]=mapped_column(
        SQLEnum(ProjectSource, name="project_source"),
        default=ProjectSource.MANUAL,
        nullable=False
    )
    # Core Info
    name: Mapped[str]=mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]]=mapped_column(Text, nullable=True)
    url: Mapped[Optional[str]]=mapped_column(String(1000), nullable=True)

    # Github Specific Fields
    github_repo_id: Mapped[Optional[int]]=mapped_column(nullable=True)
    github_full_name: Mapped[Optional[str]]=mapped_column(String(255), nullable=True)
    is_fork: Mapped[Optional[bool]]=mapped_column(nullable=True)
    stars_count: Mapped[Optional[int]]=mapped_column(nullable=True)
    forks_count: Mapped[Optional[int]]=mapped_column(nullable=True)

    # Techical details
    languages: Mapped[Optional[dict]]=mapped_column(JSON, nullable=True)  # e.g. {"Python": 12345, "JavaScript": 6789}
    primary_language: Mapped[Optional[str]]=mapped_column(String(50), nullable=True)

    # Content for analysis
    readme_content: Mapped[Optional[str]]=mapped_column(Text, nullable=True)
    readme_summary: Mapped[Optional[str]]=mapped_column(Text, nullable=True)

    # Topics
    topics: Mapped[Optional[list]]=mapped_column(JSON, nullable=True)

    # Timestamps from source
    source_created_at: Mapped[Optional[datetime]]=mapped_column(DateTime(timezone=True), nullable=True)
    source_updated_at: Mapped[Optional[datetime]]=mapped_column(DateTime(timezone=True), nullable=True)
    source_pushed_at: Mapped[Optional[datetime]]=mapped_column(DateTime(timezone=True), nullable=True)

    # Processing status
    is_proceessed: Mapped[bool]=mapped_column(nullable=False, default=False)
    is_included: Mapped[bool]=mapped_column(default=True, nullable=False)
    processing_error: Mapped[Optional[str]]=mapped_column(Text, nullable=True)

    # Relationships
    user: Mapped["User"]=relationship("User", back_populates="projects")
    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}',source={self.source.value})>"
