# /backend/auth/auth_routes.py
# Handles authentication routes (register, login, logout, refresh, check session).
# Uses JWT tokens stored in cookies for session-based authentication.

import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.data.database.db import get_db
from backend.auth.auth_queries import get_user_by_email
from backend.auth.auth_services import create_user, hash_password, verify_password, create_email_verification_token
from backend.auth.auth_models import UserRole
from backend.core.rate_limit import limiter
from backend.auth.auth_schemas import UserRead, RegisterRequest, LoginRequest, EmailRequest
from backend.user.user_models import UserProfile
from backend.auth.dependencies import get_current_user
from backend.auth.constants import RESERVED_USERNAMES
from backend.notifications import email_service
from backend.core.settings import settings


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# -----------------------------------------------------------------------------
# Dependencies
# -----------------------------------------------------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
router = APIRouter()


# -----------------------------------------------------------------------------
# Utility Functions
# -----------------------------------------------------------------------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    """Create a signed JWT refresh token."""
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return jwt.encode({"sub": user_id, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@router.get("/check")
def check_authentication(request: Request, db: Session = Depends(get_db)):
    """
    Verify if a user is currently authenticated by decoding the access token.
    Returns user email and role if valid.
    """
    token = request.cookies.get("access_token")
    if not token:
        return Response(status_code=401)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload["sub"]
        user = get_user_by_email(db, email)
        return {
            "authenticated": True,
            "email": email,
            "role": user.role.value,
        }
    except JWTError:
        return Response(status_code=401)


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user, hash password, and create linked UserProfile with username.
    Usernames are compared in lowercase against a reserved list.
    """
    if get_user_by_email(db, request.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    username_lower = request.username.lower() if request.username else None

    if username_lower in RESERVED_USERNAMES:
        raise HTTPException(status_code=400, detail="This username is reserved.")

    if (
        db.query(UserProfile)
        .filter(func.lower(UserProfile.username) == username_lower)
        .first()
    ):
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = hash_password(request.password)

    try:
        user = create_user(
            db, request.email.lower(), hashed_password, role=request.role
        )

        if db.query(UserProfile).filter_by(user_id=user.id).first():
            raise HTTPException(status_code=400, detail="Profile already exists")

        profile = UserProfile(user_id=user.id, username=request.username)
        db.add(profile)
        db.commit()
        db.refresh(profile)
        # Send email verification link
        token = create_email_verification_token(user.email)
        verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"  # Update for prod later

        email_service.send_email(
            to=user.email,
            subject="Verify your email for Fordis Ludus",
            body=f"Thanks for registering with Fordis Ludus! Please verify your email by clicking the link below:\n\n{verify_url}\n\nIf you didn’t register, you can ignore this email."
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "message": "User registered. Check your email to verify your account.",
        "next": "/login",
    }


@router.post("/login")
@limiter.limit("5/minute")
def login(
    request: Request,
    response: Response,
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    """
    Authenticate user and issue access and refresh tokens via HTTP cookies.
    """
    user = get_user_by_email(db, login_data.email)
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    if not user.is_email_verified:
        raise HTTPException(
            status_code=403,
            detail="Email not verified. Please check your email to verify your account.",
        )


    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(user.email)

    # Set tokens as cookies
    response.set_cookie(
        "access_token",
        access_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=900,
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=604800,
    )
    response.set_cookie(
        "has_session", "1", httponly=False, secure=False, samesite="Lax", max_age=604800
    )

    return {
        "message": "Login successful",
        "user": {"email": user.email, "role": user.role.value},
    }


@router.post("/refresh")
def refresh_token(request: Request, response: Response):
    """
    Refresh the user's access token using a valid refresh token.
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token found")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        new_access_token = create_access_token(data={"sub": payload["sub"]})
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=900,
        )
        return {"message": "Token refreshed"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


@router.post("/logout")
def logout(response: Response):
    """
    Clear access and refresh tokens from cookies to log the user out.
    """
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("has_session")
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserRead)
async def read_authenticated_user(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Return the authenticated user's data."""
    user_obj = get_user_by_email(db, user["email"])
    return user_obj


@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.EMAIL_VERIFICATION_ALGORITHM],
        )
        if payload.get("type") != "verify":
            raise HTTPException(status_code=400, detail="Invalid token type")

        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=400, detail="Invalid token payload")

        user = get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_email_verified:
            return {"message": "Email already verified."}

        user.is_email_verified = True
        user.email_verified_at = datetime.utcnow()
        db.commit()

        return {"message": "Email verified. Please log in."}

    except JWTError:
        raise HTTPException(
            status_code=400, detail="Invalid or expired verification token"
        )


@router.post("/resend-verification")
def resend_verification(request: EmailRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, request.email)

    if not user:
        # Do not reveal user existence
        return {
            "message": "If your account exists, a verification email has been sent."
        }

    if user.is_email_verified:
        return {"message": "Email is already verified. Please log in."}

    # Reuse token + email logic
    token = create_email_verification_token(user.email)
    verify_url = f"{settings.FRONTEND_URL}/verify-email?token={token}"

    email_service.send_email(
        to=user.email,
        subject="Verify your email for JedgeBot",
        body=f"Click to verify your email:\n\n{verify_url}",
    )

    return {"message": "Verification email has been resent. Please check your inbox."}
