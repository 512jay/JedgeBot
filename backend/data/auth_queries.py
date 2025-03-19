from sqlalchemy.orm import Session
from backend.data.auth_models import User


def get_user_by_email(db_session: Session, email: str):
    return db_session.query(User).filter(User.email == email).first()
