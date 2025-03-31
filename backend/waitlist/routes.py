# /backend/waitlist/routes.py

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from backend.waitlist import models, schemas
from backend.data.database.db import get_db

router = APIRouter(prefix="/api/waitlist", tags=["Waitlist"])


@router.post("/", response_model=schemas.WaitlistResponse, status_code=201)
def submit_waitlist_entry(
    submission: schemas.WaitlistSubmission, db: Session = Depends(get_db)
):
    existing = db.query(models.WaitlistEntry).filter_by(email=submission.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This email is already on the waitlist.",
        )

    entry = models.WaitlistEntry(**submission.dict())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
