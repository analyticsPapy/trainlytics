"""Activity model."""

import enum
from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Enum as SQLEnum, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship

from app.db.base import Base


class ActivityType(str, enum.Enum):
    """Activity type enumeration."""
    RUN = "run"
    RIDE = "ride"
    SWIM = "swim"
    WORKOUT = "workout"
    WALK = "walk"
    HIKE = "hike"
    OTHER = "other"


class DataQuality(str, enum.Enum):
    """Data quality enumeration."""
    FULL = "full"
    PARTIAL = "partial"
    MINIMAL = "minimal"


class Activity(Base):
    """Activity model."""

    __tablename__ = "activities"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    connected_account_id = Column(String, ForeignKey("connected_accounts.id"))

    # Source tracking
    provider = Column(String, nullable=False)
    provider_activity_id = Column(String, nullable=False)
    data_quality = Column(SQLEnum(DataQuality), default=DataQuality.FULL)

    # Basic metadata
    name = Column(String, nullable=False)
    description = Column(String)
    activity_type = Column(SQLEnum(ActivityType), nullable=False, index=True)
    sport_type = Column(String)

    # Date & Time
    start_date = Column(DateTime, nullable=False, index=True)
    end_date = Column(DateTime)
    timezone = Column(String)

    # Core metrics
    duration_seconds = Column(Integer)
    distance_meters = Column(Float)
    moving_time_seconds = Column(Integer)

    # Elevation
    elevation_gain_meters = Column(Float)
    elevation_loss_meters = Column(Float)

    # Heart Rate
    avg_heart_rate = Column(Integer)
    max_heart_rate = Column(Integer)

    # Power
    avg_power = Column(Float)
    max_power = Column(Float)
    normalized_power = Column(Float)

    # Speed
    avg_speed_mps = Column(Float)
    max_speed_mps = Column(Float)

    # Other
    avg_cadence = Column(Float)
    avg_temperature = Column(Float)
    calories = Column(Integer)

    # GPS
    start_latlng = Column(JSON)
    end_latlng = Column(JSON)

    # Flags
    is_manual = Column(Boolean, default=False)
    shared_with_coach = Column(Boolean, default=True)

    # Data
    available_metrics = Column(JSON, default={})
    raw_data = Column(JSON, nullable=False)
    processed_data = Column(JSON, default={})

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    synced_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="activities")
    connected_account = relationship("ConnectedAccount", back_populates="activities")
    comments = relationship("Comment", back_populates="activity")
    workout = relationship("Workout", back_populates="activity", uselist=False)

    __table_args__ = (
        Index('idx_user_provider_activity', 'user_id', 'provider_activity_id', unique=True),
    )

    def __repr__(self):
        return f"<Activity {self.name} ({self.activity_type})>"
