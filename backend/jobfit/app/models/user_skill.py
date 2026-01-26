"""
User Skill - links user to their demonstrated skills
"""
from enum import Enum
from typing import TYPE_CHECKING, Optional 
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, JSON, Enum as SQLEnum, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship 

from .base import Base 

if TYPE_CHECKING:
    from .user import User 
    from .skill import Skill

class SkillSource(str, Enum):
    """ Where the evidence was found? """
    RESUME="resume"
    GITHUB="github"
    MANUAL="manual"
    CERTIFICATION="certification"

class UserSkill(Base):
    """
    Links a user to a skill they possess with evidence.
    
    Tracks:
    - Strength/proficiency level (0-1)
    - Source of evidence (resume, GitHub, etc.)
    - Actual evidence text/references
    - Last time the skill was demonstrated

    """
    __tablename__="user_skills"

    # Foreign Keys 
    user_id: Mapped[int]=mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    skill_id: Mapped[int]=mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    # Strength/Proficiency (0-1 scale)
    # Computed from evidence quality and recency
    strength: Mapped[float]=mapped_column(default=0.5, nullable=False)

    # Primary source of evidence 
    primary_source: Mapped[SkillSource]=mapped_column(
        SQLEnum(SkillSource, name="skill_source"),
        nullable=False
    )
    # Evidence Details
    # [
    #   {"source": "resume", "text": "Built REST APIs using Django...", "similarity": 0.85},
    #   {"source": "github", "repo": "my-api", "text": "From README...", "similarity": 0.78}
    # ]
    evidence: Mapped[Optional[list]]=mapped_column(JSON, nullable=True)

    # Best evidence text (for quick display)
    best_evidence_text: Mapped[Optional[str]]=mapped_column(Text, nullable=True)
    best_evidence_similarity: Mapped[Optional[float]]=mapped_column(nullable=True)

    # Years of Experience 
    years_experience: Mapped[Optional[float]]=mapped_column(nullable=True)

    # User's self reorted proficiency (if any)
    self_reported_level: Mapped[Optional[str]]=mapped_column(nullable=True)

    # Last time this skill was seen in evidence 
    last_seen_at: Mapped[Optional[datetime]]=mapped_column(DateTime(timezone=True), nullable=True)

    # Is this skill actively being developed?
    is_learning: Mapped[bool]=mapped_column(default=False, nullable=False)

    # User Notes about this skill
    notes: Mapped[Optional[str]]=mapped_column(Text, nullable=True)

    # Realtionships
    user: Mapped["User"]=relationship("User", back_populates="skills")
    skill: Mapped["Skill"]=relationship("Skill", back_populates="user_skills")

    # Constraints
    __table_args__=(
        UniqueConstraint("user_id", "skill_id", name="uq_user_skill"),
        Index("ix_user_skills_user_strength", "user_id", "strength"),
    )
    def __repr__(self) -> str:
        return f"<UserSkill(user_id={self.user_id}, skill_id={self.skill_id}, strength={self.strength:.2f})>"