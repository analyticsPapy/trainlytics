"""Workout model."""

import enum
from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, DateTime, Enum as SQLEnum, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class WorkoutStatus(str, enum.Enum):
    """Workout status enumeration."""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    POSTPONED = "postponed"


class Workout(Base):
    """Workout model."""

    __tablename__ = "workouts"

    id = Column(String, primary_key=True, index=True)
    training_plan_id = Column(String, ForeignKey("training_plans.id"))
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    athlete_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    # Workout info
    title = Column(String, nullable=False)
    description = Column(Text)
    workout_type = Column(String, nullable=False)

    # Scheduling
    scheduled_date = Column(DateTime, nullable=False, index=True)
    scheduled_time = Column(String)

    # Target metrics
    target_duration = Column(Integer)
    target_distance = Column(Float)
    target_pace = Column(Float)
    target_heart_rate = Column(Integer)
    target_power = Column(Float)

    # Structured workout
    structure = Column(JSON)

    # Completion
    status = Column(SQLEnum(WorkoutStatus), default=WorkoutStatus.PLANNED, index=True)
    completed_at = Column(DateTime)
    activity_id = Column(String, ForeignKey("activities.id"), unique=True)

    # Feedback
    athlete_notes = Column(Text)
    coach_feedback = Column(Text)
    rpe = Column(Integer)  # Rate of Perceived Exertion (1-10)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    training_plan = relationship("TrainingPlan", back_populates="workouts")
    creator = relationship("User", foreign_keys=[created_by], back_populates="workouts_created")
    athlete = relationship("User", foreign_keys=[athlete_id], back_populates="workouts_assigned")
    activity = relationship("Activity", back_populates="workout")
    comments = relationship("Comment", back_populates="workout")

    def __repr__(self):
        return f"<Workout {self.title} for {self.athlete_id}>"
