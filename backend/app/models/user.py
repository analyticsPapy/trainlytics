"""User model."""

import enum
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""
    ATHLETE = "athlete"
    COACH = "coach"
    BOTH = "both"


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String)
    avatar_url = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.ATHLETE)
    timezone = Column(String, default="UTC")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime)

    # Relationships
    coach_profile = relationship("CoachProfile", back_populates="user", uselist=False)
    connected_accounts = relationship("ConnectedAccount", back_populates="user")
    activities = relationship("Activity", back_populates="user")

    # Coaching relationships
    coaching_as_athlete = relationship(
        "AthleteCoach",
        foreign_keys="AthleteCoach.athlete_id",
        back_populates="athlete"
    )
    coaching_as_coach = relationship(
        "AthleteCoach",
        foreign_keys="AthleteCoach.coach_id",
        back_populates="coach"
    )

    # Plans
    plans_created = relationship(
        "TrainingPlan",
        foreign_keys="TrainingPlan.created_by",
        back_populates="creator"
    )
    plans_assigned = relationship(
        "TrainingPlan",
        foreign_keys="TrainingPlan.athlete_id",
        back_populates="athlete"
    )

    # Workouts
    workouts_created = relationship(
        "Workout",
        foreign_keys="Workout.created_by",
        back_populates="creator"
    )
    workouts_assigned = relationship(
        "Workout",
        foreign_keys="Workout.athlete_id",
        back_populates="athlete"
    )

    def __repr__(self):
        return f"<User {self.email}>"
