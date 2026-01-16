"""Comment model."""

from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base import Base


class Comment(Base):
    """Comment model."""

    __tablename__ = "comments"

    id = Column(String, primary_key=True, index=True)
    author_id = Column(String, ForeignKey("users.id"), nullable=False)

    # Polymorphic - can comment on activities or workouts
    workout_id = Column(String, ForeignKey("workouts.id"))
    activity_id = Column(String, ForeignKey("activities.id"))

    content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    author = relationship("User")
    workout = relationship("Workout", back_populates="comments")
    activity = relationship("Activity", back_populates="comments")

    def __repr__(self):
        return f"<Comment by {self.author_id}>"
