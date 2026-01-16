"""Coach profile model."""

from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class CoachProfile(Base):
    """Coach profile model."""

    __tablename__ = "coach_profiles"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), unique=True, nullable=False)

    bio = Column(Text)
    specialties = Column(Text)  # Comma-separated
    max_athletes = Column(Integer, default=10)
    accepting_new = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="coach_profile")

    def __repr__(self):
        return f"<CoachProfile {self.user_id}>"
