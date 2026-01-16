"""Training plan model."""

import enum
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime, Enum as SQLEnum, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class PlanStatus(str, enum.Enum):
    """Training plan status enumeration."""
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class TrainingPlan(Base):
    """Training plan model."""

    __tablename__ = "training_plans"

    id = Column(String, primary_key=True, index=True)
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    athlete_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    name = Column(String, nullable=False)
    description = Column(Text)

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    weeks_count = Column(Integer)

    is_template = Column(Boolean, default=False)
    status = Column(SQLEnum(PlanStatus), default=PlanStatus.DRAFT)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    creator = relationship("User", foreign_keys=[created_by], back_populates="plans_created")
    athlete = relationship("User", foreign_keys=[athlete_id], back_populates="plans_assigned")
    workouts = relationship("Workout", back_populates="training_plan")

    def __repr__(self):
        return f"<TrainingPlan {self.name} for {self.athlete_id}>"
