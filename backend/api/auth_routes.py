# /backend/api/auth_routes.py
# Handles authentication routes (register, login, logout, refresh, check session).
# Uses JWT tokens stored in cookies for session-based authentication.

import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from backend.data.database.auth.auth_db import get_db
from backend.data.database.auth.auth_queries import get_user_by_email
from backend.data.database.auth.auth_services import create_user
from backend.data.database.auth.auth_services import hash_password, verify_password


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
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


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


def get_current_user(request: Request) -> dict:
    """Extract the current user from the access_token cookie."""
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    try:
        payload = jwt.decode(
            token.replace("Bearer ", ""), SECRET_KEY, algorithms=[ALGORITHM]
        )
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": user_email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@router.get("/check")
def check_authentication(request: Request):
    """
    Verify if a user is currently authenticated.
    Returns email if valid, 401 if not.
    """
    token = request.cookies.get("access_token")
    if not token:
        return Response(status_code=401)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"authenticated": True, "email": payload["sub"]}
    except JWTError:
        return Response(status_code=401)


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user with email and password.
    """
    if get_user_by_email(db, request.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(request.password)
    try:
        new_user = create_user(db, request.email, hashed_password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "User registered successfully"}


@router.post("/login")
def login(response: Response, login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and issue access and refresh tokens via HTTP cookies.
    """
    user = get_user_by_email(db, login_data.email)
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(user.email)

    # Set tokens as secure cookies
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

    return {"message": "Login successful"}


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
    Clear both access and refresh tokens from cookies to log the user out.
    """
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}
