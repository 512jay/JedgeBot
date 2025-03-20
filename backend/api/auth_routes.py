# /backend/api/auth_routes.py
# Handles authentication routes (login, logout, refresh token).

import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from jose import JWTError, jwt
from backend.data.database.authorization.auth_schema import User
from backend.data.database.authorization.auth_queries import get_user_by_email

# Environment variables (Use a .env file for production)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for dependency injection
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str

# Hash passwords
def hash_password(password: str):
    return pwd_context.hash(password)


# Verify passwords
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Create JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Create refresh token
def create_refresh_token(user_id: str):
    return jwt.encode(
        {
            "sub": user_id,
            "exp": datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        },
        SECRET_KEY,
        algorithm=ALGORITHM,
    )

# get current user
def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        payload = jwt.decode(
            token.replace("Bearer ", ""), SECRET_KEY, algorithms=[ALGORITHM]
        )
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    return {"email": user_email}  # Modify if user lookup is needed


@router.post("/login")
def login(response: Response, request: Request, login_data: LoginRequest):
    db_session = SessionLocal()  # Create a new session
    user = get_user_by_email(db_session, login_data.email)
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(user.email)

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,  # Use HTTPS in production
        samesite="Strict",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Strict",
    )

    return {"message": "Login successful"}


@router.post("/auth/refresh")
def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token found")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        new_access_token = create_access_token(data={"sub": payload["sub"]})

        response.set_cookie(
            key="access_token",
            value=f"Bearer {new_access_token}",
            httponly=True,
            secure=True,
            samesite="Strict",
        )

        return {"message": "Token refreshed"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}
