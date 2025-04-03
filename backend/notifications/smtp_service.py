# /backend/notifications/smtp_service.py
# Utility for sending emails via SMTP using smtplib and settings.

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.core.settings import settings


def send_email(*, subject: str, to: str, body: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.EMAIL_FROM
    msg["To"] = to

    part = MIMEText(body, "html")
    msg.attach(part)

    try:
        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_FROM, settings.EMAIL_PASSWORD)
            server.sendmail(settings.EMAIL_FROM, to, msg.as_string())
            print(f"✅ Email sent to {to}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
