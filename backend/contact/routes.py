# /backend/contact/routes.py

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, EmailStr
from backend.notifications.smtp_service import send_email
from backend.core.rate_limit import limiter

router = APIRouter()


class ContactMessage(BaseModel):
    email: EmailStr
    message: str


@limiter.limit("3/minute")
@router.post("/contact", status_code=status.HTTP_200_OK)
def contact_form(data: ContactMessage):
    send_email(
        to="admin@fordisludus.com",
        subject=f"Contact Form Submission from {data.email}",
        body=data.message,
    )
    return {"message": "Your message has been sent successfully."}
