from sqlalchemy.orm import Session
from backend.data.database.auth.auth_schema import User


def get_user_by_email(db_session: Session, email: str):
    return db_session.query(User).filter(User.email == email).first()


def create_user(db_session: Session, email: str, password_hash: str):
    new_user = User(email=email, password_hash=password_hash)
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return new_user
