"""Athlete-Coach relationship model."""

import enum
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.base import Base


class CoachingStatus(str, enum.Enum):
    """Coaching status enumeration."""
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"
    REJECTED = "rejected"


class AthleteCoach(Base):
    """Athlete-Coach relationship model."""

    __tablename__ = "athlete_coaches"

    id = Column(String, primary_key=True, index=True)
    athlete_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    coach_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    status = Column(SQLEnum(CoachingStatus), default=CoachingStatus.PENDING)
    permissions = Column(JSON, default={})  # View activities, create workouts, etc.

    start_date = Column(DateTime)
    end_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    athlete = relationship("User", foreign_keys=[athlete_id], back_populates="coaching_as_athlete")
    coach = relationship("User", foreign_keys=[coach_id], back_populates="coaching_as_coach")

    def __repr__(self):
        return f"<AthleteCoach athlete={self.athlete_id} coach={self.coach_id}>"
