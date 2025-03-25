# /backend/data/database/auth/auth_services.py
# Business logic layer for authentication actions and workflows.

from datetime import datetime
from sqlalchemy.orm import Session
from backend.auth.models import User, UserRole
from backend.auth.auth_queries import get_user_by_email
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)


def create_user(
    db: Session, email: str, password_hash: str, role: UserRole = UserRole.FREE
) -> User:
    """
    Creates a new user in the database if the email is not already taken.

    Args:
        db (Session): SQLAlchemy database session
        email (str): The user's email address
        password_hash (str): Hashed password (bcrypt)
        role (UserRole): The role to assign the user (default is FREE)

    Returns:
        User: The newly created user object

    Raises:
        ValueError: If a user with the given email already exists
    """
    existing = get_user_by_email(db, email)
    if existing:
        raise ValueError("User with this email already exists.")

    user = User(email=email, password_hash=password_hash, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_last_login(db: Session, user: User) -> User:
    """
    Updates the last_login timestamp for the user.

    Args:
        db (Session): SQLAlchemy session
        user (User): User object to update

    Returns:
        User: The updated user object
    """
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def deactivate_user(db: Session, user: User) -> User:
    """
    Deactivates a user account.

    Args:
        db (Session): SQLAlchemy session
        user (User): User to deactivate

    Returns:
        User: The updated user object
    """
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    """
    Permanently deletes a user account from the database.

    Args:
        db (Session): SQLAlchemy session
        user (User): User to delete
    """
    db.delete(user)
    db.commit()


def change_user_role(db: Session, user: User, new_role: UserRole) -> User:
    """
    Changes the role of a user.

    Args:
        db (Session): SQLAlchemy session
        user (User): User to update
        new_role (UserRole): New role to assign

    Returns:
        User: The updated user object
    """
    user.role = new_role
    db.commit()
    db.refresh(user)
    return user


def get_or_create_user(
    db: Session, email: str, password_hash: str, role: UserRole = UserRole.FREE
) -> User:
    """
    Retrieves a user by email or creates a new one if not found.

    Args:
        db (Session): SQLAlchemy session
        email (str): Email to search for
        password_hash (str): Hashed password (if new user)
        role (UserRole): Role to assign if created

    Returns:
        User: The existing or newly created user object
    """
    user = get_user_by_email(db, email)
    if user:
        return user
    return create_user(db, email, password_hash, role)

# TODO: Implement password reset functionality, including generating and validating reset tokens.
# TODO: Implement email verification functionality, including generating and validating verification tokens.
# TODO: Implement user profile management, allowing users to update their information.
# TODO: Implement logging for all user actions (login, logout, password change, etc.).
# TODO: Implement rate limiting for login attempts to prevent brute force attacks.
# TODO: Implement multi-factor authentication (MFA) for added security.
# TODO: Implement OAuth2 or other third-party authentication methods for user convenience.
# TODO: Implement user activity tracking to monitor and analyze user behavior.
# TODO: Implement API rate limiting to prevent abuse of the authentication endpoints.
# TODO: Implement session management to handle user sessions securely.
# TODO: Implement CSRF protection for web-based authentication flows.
# TODO: Implement secure storage and handling of sensitive user data (e.g., passwords, tokens).
# TODO: Implement logging and monitoring for security-related events (e.g., failed login attempts, account lockouts).
# TODO: Implement a mechanism for users to delete their accounts and associated data.
# TODO: Implement a mechanism for administrators to manage user accounts (e.g., view, edit, delete).
# TODO: Implement a mechanism for users to recover their accounts in case of forgotten passwords or locked accounts.
# TODO: Implement a mechanism for users to update their email addresses.
# TODO: Implement a mechanism for users to update their passwords.
# TODO: Implement a mechanism for users to manage their notification preferences.
# TODO: Implement a mechanism for users to manage their privacy settings.
# TODO: Implement a mechanism for users to manage their security settings (e.g., change password, enable/disable MFA).
# TODO: Implement a mechanism for users to manage their connected applications (e.g., revoke access).
# TODO: Implement a mechanism for users to manage their API keys.
# TODO: Implement a mechanism for users to manage their access tokens.
# TODO: Implement a mechanism for users to manage their refresh tokens.
# TODO: Implement a mechanism for users to manage their session tokens.
# TODO: Implement a mechanism for users to manage their login history.
# TODO: Implement a mechanism for users to manage their account activity.
# TODO: Implement a mechanism for users to manage their account settings.
# TODO: Implement a mechanism for users to manage their account preferences.
# TODO: Implement a mechanism for users to manage their account notifications.
# TODO: Implement a mechanism for users to manage their account security.
# TODO: Implement a mechanism for users to manage their account privacy.
# If/when you implement audit logging, this is the file where those log_event(...) calls will go — and it’s already designed to support it
