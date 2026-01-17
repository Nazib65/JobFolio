"""
Resume Model for uploaded user resumes
"""
from ctypes import Structure
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Text, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User 

class Resume(Base):
    """
    Represents an uploaded resume document
    """
    __tablename__="resumes"

    # ownership 
    user_id: Mapped[int]=mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    # File storage
    file_path: Mapped[str]=mapped_column(String(500), nullable=False)
    file_name: Mapped[str]=mapped_column(String(255), nullable=False)
    file_size_bytes: Mapped[Optional[int]]=mapped_column(nullable=True)
    file_hash: Mapped[Optional[str]]=mapped_column(String(64), nullable=True)
    mime_type: Mapped[Optional[str]]=mapped_column(String(100), nullable=True)

    # Extracted Content
    raw_text: Mapped[Optional[str]]=mapped_column(Text, nullable=True)

    # Parsed Structure (JSON)
    # Structure:
    # {
    #   "contact": {"name": "...", "email": "...", "phone": "...", "linkedin": "..."},
    #   "summary": "...",
    #   "experience": [
    #     {"company": "...", "title": "...", "start": "...", "end": "...", "bullets": [...]}
    #   ],
    #   "education": [
    #     {"institution": "...", "degree": "...", "field": "...", "year": "..."}
    #   ],
    #   "skills_section": [...],  # Raw skills listed in resume
    #   "certifications": [...],
    #   "projects": [...]
    # }

    parsed_JSON: Mapped[Optional[dict]]=mapped_column(JSON, nullable=True)
    
    # Bullet Points for Embedding (each experience bullet as separate item)
    # [{"text": "...", "context": "company_name - title", "embedding_id": "..."}]
    
    bullet_points: Mapped[Optional[list]]=mapped_column(JSON, nullable=True)

    # Processing Status
    is_active: Mapped[bool]=mapped_column(default=True, nullable=False)
    is_processed: Mapped[bool]=mapped_column(default=False, nullable=False)
    processing_error: Mapped[Optional[str]]=mapped_column(Text, nullable=True)

    # Label (for people with multiple resumes)
    label: Mapped[Optional[str]]=mapped_column(String(100), nullable=True)

    # Realtionships
    user: Mapped["User"]=relationship("User", back_populates="resumes")

    def __repr__(self) -> str:
        return f"<Resume id={self.id}, user_id={self.user_id}, file_name='{self.file_name}'>"