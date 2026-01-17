"""
Skill model for the canonical skills catalog
"""
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON, String, Text, Enum as SQLEnum, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user_skill import UserSkill
    from .job_skill import JobSkill

class SkillCategory(str, Enum):
    """
    Primary Category for skills
    Maps to radar chart dimensions
    """
    # Technical categories
    LANGUAGE="language"
    FRAMEWORK="framework"
    CLOUD="cloud"
    TOOL="tool"
    DEVOPS="devops"
    ML_AI="ml_ai"
    PLATFORM="platform"
    DATABASE="database"
    FRONTEND="frontend"
    BACKEND="backend"
    MOBILE="mobile"
    SECURITY="security"
    DATA_SCIENCE="data_science"
    DATA="data"
    Testing="testing"

    # soft skill categories
    SOFT_SKILL="soft_skill"
    MANAGEMENT="management"
    COMMUNICATION="communication"
    LEADERSHIP="leadership"
    METHODLOGY="methodology"
    DOMAIN="domain"

   # Other
    OTHER="other"

class SkillLevel(str, Enum):
    """
    Proficiency levels for skills
    """
    BEGINNER="beginner"
    INTERMEDIATE="intermediate"
    ADVANCED="advanced"
    EXPERT="expert"

class Skill(Base):
    """
    Canonical skill definition.
    
    Used to normalize various spellings/aliases to a single canonical form.
    Example: "JS", "JavaScript", "java script" all map to canonical "JavaScript".
    """
    __tablename__="skills"

    # Canonical name
    canonical_name: Mapped[str]=mapped_column(String(255), unique=True, nullable=False, index=True)

    # Dsisplay name (may differ from canonical for UI purposes)
    display_name: Mapped[Optional[str]]=mapped_column(String(255), nullable=True)

    # Category for grouping and radar chart mapping
    category: Mapped[SkillCategory]=mapped_column(
        SQLEnum(SkillCategory, name="skill_category"),
        nullable=False,
        index=True
    )
    # Sub category for more granular grouping
    sub_category: Mapped[Optional[str]]=mapped_column(String(255), nullable=True)

    # Aliases (alternative names/spellings)
    # ["JS", "javascript", "java script", "ECMAScript"]
    aliases: Mapped[Optional[list]]=mapped_column(JSON, nullable=True)

     # Related skills (for recommendations)
    # ["TypeScript", "Node.js", "React"]
    related_skills: Mapped[Optional[list]]=mapped_column(JSON, nullable=True)

    # Description for tooltip 
    description: Mapped[Optional[str]]=mapped_column(Text, nullable=True)

    # Icon Url for UI
    icon_url: Mapped[Optional[str]]=mapped_column(String(500), nullable=True)

    # Official documentation URL
    documentation_url: Mapped[Optional[str]]=mapped_column(String(1000), nullable=True)

    # Is this a hot skill in the current market?
    is_hot_skill: Mapped[bool]=mapped_column(default=False, nullable=False)

    # Skill popularity/weight (for ranking)
    popularity_score: Mapped[Optional[float]]=mapped_column(nullable=True)

    # Realtionships 
    user_skills: Mapped[list["UserSkill"]]=relationship(
        "UserSkill",
        back_populates="skill",
        cascade="all, delete-orphan"
    )
    job_skills: Mapped[list["JobSkill"]]=relationship(
        "JobSkill",
        back_populates="skill",
        cascade="all, delete-orphan"
    )

    # Composite index for category and name lookups
    __table_args__=(
        Index("ix_skill_category_name", "category", "canonical_name"),
    )
    def __repr__(self) -> str:
        return f"<Skill(id={self.id}, canonical_name='{self.canonical_name}', category={self.category.value})>"
