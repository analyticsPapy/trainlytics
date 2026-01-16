"""Connected account model for external integrations."""

import enum
from datetime import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Provider(str, enum.Enum):
    """Provider enumeration."""
    STRAVA = "strava"
    GARMIN = "garmin"
    POLAR = "polar"
    COROS = "coros"
    MANUAL = "manual"


class ConnectedAccount(Base):
    """Connected account model."""

    __tablename__ = "connected_accounts"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)

    provider = Column(SQLEnum(Provider), nullable=False)
    provider_user_id = Column(String, nullable=False)
    provider_username = Column(String)

    # Encrypted tokens
    access_token = Column(String, nullable=False)
    refresh_token = Column(String)
    token_expires_at = Column(Integer)

    # Sync settings
    sync_enabled = Column(Boolean, default=True)
    last_sync_at = Column(DateTime)
    last_sync_status = Column(String)

    is_active = Column(Boolean, default=True)
    connected_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="connected_accounts")
    activities = relationship("Activity", back_populates="connected_account")

    def __repr__(self):
        return f"<ConnectedAccount {self.provider} for {self.user_id}>"
