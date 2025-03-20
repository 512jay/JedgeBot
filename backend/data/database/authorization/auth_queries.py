from sqlalchemy.orm import Session
from backend.data.database.authorization.auth_schema import User


def get_user_by_email(db_session: Session, email: str):
    return db_session.query(User).filter(User.email == email).first()
