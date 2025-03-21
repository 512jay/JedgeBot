# /backend/api/auth_routes.py
# Handles authentication routes (login, logout, refresh token).

import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from pydantic import BaseModel
from jose import JWTError, jwt
from backend.data.database.auth.auth_schema import User
from backend.data.database.auth.auth_queries import get_user_by_email, create_user
from backend.data.database.auth.auth_db import SessionLocal


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


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str


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

@router.get("/check")  # ✅ Fix: remove extra "/auth"
def check_authentication(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        print("❌ No access_token found in cookies")
        return Response(status_code=401)

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"authenticated": True, "email": payload["sub"]}
    except JWTError:
        print("❌ Invalid or expired token")
        return Response(status_code=401)


@router.post("/login")
def login(response: Response, request: Request, login_data: LoginRequest):
    db_session = SessionLocal()
    user = get_user_by_email(db_session, login_data.email)
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(user.email)

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # 🔒 Change to True in production
        samesite="Lax",
        max_age=900,  # 15 min expiration
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=604800,  # 7-day expiration
    )

    return {"message": "Login successful"}


@router.post("/register")
def register(request: RegisterRequest):
    db_session = SessionLocal()
    existing_user = get_user_by_email(db_session, request.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(request.password)
    new_user = create_user(db_session, request.email, hashed_password)

    if not new_user:
        raise HTTPException(status_code=500, detail="User registration failed")

    return {"message": "User registered successfully"}


@router.post("/refresh")
def refresh_token(request: Request, response: Response):
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
            max_age=900,  # 15 min expiration
        )

        return {"message": "Token refreshed"}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}
