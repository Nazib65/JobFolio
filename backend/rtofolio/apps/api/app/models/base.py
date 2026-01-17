"""
Base Model with common fields and utilities
"""
from datetime import datetime 
from typing import Any
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """
    Base class for all database models.
    Provides common fields and utilities.
    """
    id: Mapped[int]=mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime]=mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        opupdate=func.now(),
        nullable=False
    )
    def to_dict(self) -> dict[str, Any]:
        """ Covert model to dictionary """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}