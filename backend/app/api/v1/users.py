"""User endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter()


@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "role": current_user.role,
        "avatar_url": current_user.avatar_url,
        "timezone": current_user.timezone,
        "created_at": current_user.created_at,
        "last_login_at": current_user.last_login_at
    }
