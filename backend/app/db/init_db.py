"""Database initialization."""

from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import engine
from app.models.user import User, UserRole
from app.core.security import get_password_hash
import uuid


def init_db(db: Session) -> None:
    """Initialize database with default data."""
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Check if admin user exists
    admin = db.query(User).filter(User.email == "admin@trainlytics.com").first()

    if not admin:
        # Create default admin user
        admin = User(
            id=str(uuid.uuid4()),
            email="admin@trainlytics.com",
            hashed_password=get_password_hash("admin123"),
            name="Admin User",
            role=UserRole.BOTH
        )
        db.add(admin)
        db.commit()
        print("✅ Admin user created: admin@trainlytics.com / admin123")
    else:
        print("ℹ️  Admin user already exists")
