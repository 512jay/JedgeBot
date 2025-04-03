# /backend/waitlist/routes.py

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from backend.waitlist import models, schemas
from backend.data.database.db import get_db
from backend.notifications.smtp_service import send_email

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

    entry = models.WaitlistEntry(**submission.model_dump())

    db.add(entry)
    db.commit()
    db.refresh(entry)

    # ✉️ Notify admin via email
    send_email(
        to="admin@fordisludus.com",
        subject="New Waitlist Signup",
        body=f"""\
A new user has joined the waitlist:

Name: {submission.name}
Email: {submission.email}
Role: {submission.role}
Feedback: {submission.feedback or "None"}

View in database or follow up manually.
""",
    )

    return entry
