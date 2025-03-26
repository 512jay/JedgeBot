# /backend/maintenance/cleanup.py
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from backend.auth.password.models import PasswordResetToken


def cleanup_password_reset_tokens(db: Session) -> int:
    """
    Deletes used or expired password reset tokens from the database.

    Returns:
        int: number of rows deleted
    """
    q = db.query(PasswordResetToken).filter(
        (PasswordResetToken.used == True)
        | (PasswordResetToken.expires_at < datetime.now(timezone.utc))
    )
    count = q.count()
    q.delete(synchronize_session=False)
    db.commit()
    return count
