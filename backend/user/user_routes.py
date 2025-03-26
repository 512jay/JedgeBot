# /backend/user/user_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.user.user_models import UserProfile
from backend.user.user_schemas import UserProfileCreate, UserProfileRead
from backend.auth.dependencies import get_current_user  # assumes this exists
from backend.data.database.models import Base  # ensures same session
from backend.auth.auth_models import User
from backend.data.database.db import get_db  # your DB session

router = APIRouter()


@router.post("/profiles/init", response_model=UserProfileRead)
def init_profile(
    profile_data: UserProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if db.query(UserProfile).filter_by(user_id=current_user.id).first():
        raise HTTPException(status_code=400, detail="Profile already exists")

    profile = UserProfile(user_id=current_user.id, **profile_data.dict())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@router.get("/profiles/me", response_model=UserProfileRead)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = db.query(UserProfile).filter_by(user_id=current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
# /backend/user/user_routes.py
# Compare this snippet from backend/data/database/models.py: