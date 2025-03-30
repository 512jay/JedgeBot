# /backend/auth/password/tests/test_password_reset_service.py
# Unit tests for password reset token generation and validation logic.

from backend.auth.password.service import (
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


def test_validate_invalid_token_raises(get_db_session):
    from backend.auth.password.service import validate_token
    import pytest

    with pytest.raises(ValueError, match="Invalid or unknown token"):
        validate_token("this-is-fake", db=get_db_session)


def test_used_token_raises(get_db_session, free_user):
    from backend.auth.password.service import (
        create_password_reset_token,
        validate_token,
    )
    from backend.auth.auth_models import User
    from backend.auth.password.service import mark_token_as_used
    import pytest

    user = get_db_session.query(User).filter_by(email=free_user["email"]).first()
    token = create_password_reset_token(get_db_session, user)
    mark_token_as_used(get_db_session, token)

    with pytest.raises(ValueError, match="already been used"):
        validate_token(token, db=get_db_session)
