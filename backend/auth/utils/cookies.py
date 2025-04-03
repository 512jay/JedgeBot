# /backend/auth/utils/cookies.py
# Centralized helper for setting authentication cookies.

from fastapi import Response
from backend.core.settings import settings


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    """
    Set secure HTTP-only cookies for access and refresh tokens.
    """
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=settings.is_production,
        samesite="None" if settings.is_production else "Lax",
        max_age=900,  # 15 minutes
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.is_production,
        samesite="None" if settings.is_production else "Lax",
        max_age=604800,  # 7 days
    )
    # Optional UI-friendly cookie to show "signed in" state
    response.set_cookie(
        key="has_session",
        value="1",
        httponly=False,
        secure=False,
        samesite="Lax",
        max_age=604800,
    )


def clear_auth_cookies(response: Response) -> None:
    base_settings = {
        "path": "/",
        "samesite": "strict",
    }

    # Secure cookies for auth tokens
    secure_settings = base_settings.copy()
    secure_settings["httponly"] = True
    if settings.is_production:
        secure_settings["secure"] = True
        secure_settings["samesite"] = "none"

    response.delete_cookie("access_token", **secure_settings)
    response.delete_cookie("refresh_token", **secure_settings)

    # Also delete has_session (not httponly)
    session_cookie_settings = base_settings.copy()
    session_cookie_settings["httponly"] = False
    session_cookie_settings["secure"] = settings.is_production
    session_cookie_settings["samesite"] = "none" if settings.is_production else "lax"

    response.delete_cookie("has_session", **session_cookie_settings)
