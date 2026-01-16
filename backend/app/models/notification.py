"""Notification model."""

import enum
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime, Enum as SQLEnum, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class NotificationType(str, enum.Enum):
    """Notification type enumeration."""
    WORKOUT_ASSIGNED = "workout_assigned"
    WORKOUT_COMMENT = "workout_comment"
    ACTIVITY_COMMENT = "activity_comment"
    PLAN_CREATED = "plan_created"
    COACHING_INVITATION = "coaching_invitation"
    COACHING_ACCEPTED = "coaching_accepted"
    SYNC_COMPLETED = "sync_completed"
    SYNC_FAILED = "sync_failed"


class Notification(Base):
    """Notification model."""

    __tablename__ = "notifications"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    type = Column(SQLEnum(NotificationType), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    action_url = Column(String)

    is_read = Column(Boolean, default=False, index=True)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User")

    def __repr__(self):
        return f"<Notification {self.type} for {self.user_id}>"
