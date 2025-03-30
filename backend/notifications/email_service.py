# /backend/notifications/email_service.py
# Handles development email sending via MailHog's local SMTP server.

import smtplib
from email.message import EmailMessage


def send_email(to: str, subject: str, body: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "noreply@jedgebot.local"
    msg["To"] = to
    msg.set_content(body)

    with smtplib.SMTP("localhost", 1025) as smtp:
        smtp.send_message(msg)
