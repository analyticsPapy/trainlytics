"""Database models."""

from app.models.user import User, UserRole
from app.models.coach_profile import CoachProfile
from app.models.athlete_coach import AthleteCoach, CoachingStatus
from app.models.connected_account import ConnectedAccount, Provider
from app.models.activity import Activity, ActivityType, DataQuality
from app.models.workout import Workout, WorkoutStatus
from app.models.training_plan import TrainingPlan, PlanStatus
from app.models.comment import Comment
from app.models.notification import Notification, NotificationType

__all__ = [
    "User",
    "UserRole",
    "CoachProfile",
    "AthleteCoach",
    "CoachingStatus",
    "ConnectedAccount",
    "Provider",
    "Activity",
    "ActivityType",
    "DataQuality",
    "Workout",
    "WorkoutStatus",
    "TrainingPlan",
    "PlanStatus",
    "Comment",
    "Notification",
    "NotificationType",
]
