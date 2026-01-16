"""Workout endpoints."""

from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.workout import Workout, WorkoutStatus

router = APIRouter()


@router.get("/")
async def get_workouts(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status_filter: Optional[WorkoutStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's workouts."""
    query = db.query(Workout).filter(Workout.athlete_id == current_user.id)

    if status_filter:
        query = query.filter(Workout.status == status_filter)

    query = query.order_by(Workout.scheduled_date.desc())
    workouts = query.offset(skip).limit(limit).all()

    return [
        {
            "id": w.id,
            "title": w.title,
            "workout_type": w.workout_type,
            "scheduled_date": w.scheduled_date,
            "status": w.status,
            "target_duration": w.target_duration,
            "target_distance": w.target_distance,
        }
        for w in workouts
    ]


@router.get("/{workout_id}")
async def get_workout(
    workout_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get workout details."""
    workout = db.query(Workout).filter(Workout.id == workout_id).first()

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout not found"
        )

    # Check permissions (athlete or coach)
    if workout.athlete_id != current_user.id and workout.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this workout"
        )

    return {
        "id": workout.id,
        "title": workout.title,
        "description": workout.description,
        "workout_type": workout.workout_type,
        "scheduled_date": workout.scheduled_date,
        "status": workout.status,
        "target_duration": workout.target_duration,
        "target_distance": workout.target_distance,
        "target_pace": workout.target_pace,
        "target_heart_rate": workout.target_heart_rate,
        "structure": workout.structure,
        "athlete_notes": workout.athlete_notes,
        "coach_feedback": workout.coach_feedback,
        "rpe": workout.rpe,
        "created_at": workout.created_at
    }
