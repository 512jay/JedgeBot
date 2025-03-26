# /backend/auth/password_reset/tests/test_password_reset_service.py
# Unit tests for password reset token generation and validation logic.

from backend.auth.password_reset.service import (
    create_password_reset_token,
    validate_token,
)
from backend.auth.auth_models import User


def test_create_and_validate_token(get_db_session, free_user):
    # Retrieve the user from the DB using the fixture-created email
    user = get_db_session.query(User).filter_by(email=free_user["email"]).first()

    # Generate a token for that user
    token = create_password_reset_token(get_db_session, user)

    # Validate that token
    validated_user = validate_token(token, db=get_db_session)

    # Confirm the validated user is the same as the one the token was created for
    assert validated_user.id == user.id
