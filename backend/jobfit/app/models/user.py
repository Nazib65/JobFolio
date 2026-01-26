"""
User model representing authenticated users
"""
from datetime import datetime
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped,mapped_column, relationship

from .base import Base 

if TYPE_CHECKING:
    from .analysis import Analysis 
    from .resume import Resume 
    from .project import Project
    from .user_skill import UserSkill

class User(Base):
    """
    Represents a registered user in the system
    """
    __tablename__="users"

    # Authentication and identification
    email: Mapped[str]=mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str]=mapped_column(String(255), nullable=False)
    hashed_password: Mapped[Optional[str]]=mapped_column(String(255), nullable=True)

    # Github Integration 
    github_username: Mapped[Optional[str]]=mapped_column(String(100), nullable=True, index=True)
    github_access_token: Mapped[Optional[str]]=mapped_column(Text, nullable=True)
    is_github_connected: Mapped[bool]=mapped_column(default=False, nullable=False)
    github_connected_at: Mapped[Optional[datetime]]=mapped_column(nullable=True)

    # Profile 
    avatar_url: Mapped[Optional[str]]=mapped_column(String(500), nullable=True)
    headline: Mapped[Optional[str]]=mapped_column(String(500), nullable=True)
    bio: Mapped[Optional[str]]=mapped_column(Text, nullable=True)
    location: Mapped[Optional[str]]=mapped_column(String(255), nullable=True)

    # Account status
    is_active: Mapped[bool]=mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool]=mapped_column(Boolean, default=False, nullable=False)

    # Realtionships
    resumes: Mapped[list["Resume"]]=relationship(
        "Resume",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    projects: Mapped[list["Project"]]=relationship(
        "Project",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    analyses: Mapped[list["Analysis"]]=relationship(
        "Analysis",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    skills: Mapped[list["UserSkill"]]=relationship(
        "UserSkill",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"<User (id={self.id}, email='{self.email}', name='{self.name}')>"