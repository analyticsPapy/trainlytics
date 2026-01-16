"""SQLAlchemy base class."""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models here for Alembic
from app.models.user import User  # noqa
from app.models.coach_profile import CoachProfile  # noqa
from app.models.athlete_coach import AthleteCoach  # noqa
from app.models.connected_account import ConnectedAccount  # noqa
from app.models.activity import Activity  # noqa
from app.models.workout import Workout  # noqa
from app.models.training_plan import TrainingPlan  # noqa
from app.models.comment import Comment  # noqa
from app.models.notification import Notification  # noqa
