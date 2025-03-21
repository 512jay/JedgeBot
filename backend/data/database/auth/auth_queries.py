# /backend/data/database/auth/auth_queries.py
# Queries for user management in the authentication database.

from sqlalchemy.orm import Session
from backend.data.database.auth.models import User


def get_user_by_email(db_session: Session, email: str):
    return db_session.query(User).filter(User.email == email).first()


# auth_queries.py
def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()


def list_users_by_role(db: Session, role: UserRole):
    return db.query(User).filter(User.role == role).all()


def update_last_login(db: Session, user: User):
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user
