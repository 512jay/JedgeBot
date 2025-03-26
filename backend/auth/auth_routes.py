# /backend/auth/auth_routes.py
# Handles authentication routes (register, login, logout, refresh, check session).
# Uses JWT tokens stored in cookies for session-based authentication.

import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from slowapi import Limiter
from slowapi.util import get_remote_address
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend.data.database.db import get_db
from backend.auth.auth_queries import get_user_by_email
from backend.auth.auth_services import create_user, hash_password, verify_password
from backend.auth.auth_models import UserRole
from backend.core.rate_limit import limiter
from backend.auth.auth_schemas import UserRead
from backend.user.user_models import UserProfile
from backend.auth.dependencies import get_current_user


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
# Schemas
# -----------------------------------------------------------------------------
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=6, description="Password must be at least 6 characters"
    )
    role: UserRole
    username: Optional[str]


class LoginRequest(BaseModel):
    """Schema for user login request."""

    email: str
    password: str


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
    """
    if get_user_by_email(db, request.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(request.password)

    try:
        user = create_user(
            db, request.email.lower(), hashed_password, role=request.role
        )

        if db.query(UserProfile).filter_by(user_id=user.id).first():
            raise HTTPException(status_code=400, detail="Profile already exists")

        profile = UserProfile(user_id=user.id, username=request.username)
        # TODO: Expand profile creation to use more fields as onboarding evolves
        db.add(profile)
        db.commit()
        db.refresh(profile)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "message": f"User registered successfully as {request.role.value}",
        "profile_id": str(profile.id),
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
