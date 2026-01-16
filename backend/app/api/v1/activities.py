"""Activity endpoints."""

from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.activity import Activity, ActivityType

router = APIRouter()


@router.get("/")
async def get_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    activity_type: Optional[ActivityType] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's activities."""
    query = db.query(Activity).filter(Activity.user_id == current_user.id)

    if activity_type:
        query = query.filter(Activity.activity_type == activity_type)

    query = query.order_by(Activity.start_date.desc())
    activities = query.offset(skip).limit(limit).all()

    return [
        {
            "id": a.id,
            "name": a.name,
            "activity_type": a.activity_type,
            "start_date": a.start_date,
            "duration_seconds": a.duration_seconds,
            "distance_meters": a.distance_meters,
            "provider": a.provider,
        }
        for a in activities
    ]


@router.get("/{activity_id}")
async def get_activity(
    activity_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get activity details."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )

    # Check permissions
    if activity.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this activity"
        )

    return {
        "id": activity.id,
        "name": activity.name,
        "description": activity.description,
        "activity_type": activity.activity_type,
        "start_date": activity.start_date,
        "duration_seconds": activity.duration_seconds,
        "distance_meters": activity.distance_meters,
        "elevation_gain_meters": activity.elevation_gain_meters,
        "avg_heart_rate": activity.avg_heart_rate,
        "max_heart_rate": activity.max_heart_rate,
        "avg_power": activity.avg_power,
        "avg_speed_mps": activity.avg_speed_mps,
        "calories": activity.calories,
        "provider": activity.provider,
        "created_at": activity.created_at
    }
