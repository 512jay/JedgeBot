# jedgebot/api/auth.py
import os
import re
import sqlite3
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional


# Secret key for JWT (Replace this with a secure key in production)
SECRET_KEY = os.getenv(
    "SECRET_KEY", secrets.token_hex(32)
)  # ✅ Generate or load secure key

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()


class User(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class PasswordResetRequest(BaseModel):
    username: str


class PasswordResetData(BaseModel):
    new_password: str


def get_current_user(token: str = Depends(oauth2_scheme)):
    """Retrieve the currently authenticated user."""
    conn = get_auth_db()
    cursor = conn.cursor()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if not username:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )

        # ✅ Check if token exists in the database
        cursor.execute(
            "SELECT * FROM tokens WHERE username = ? AND token = ?",
            (username, token),
        )
        valid_token = cursor.fetchone()
        if not valid_token:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    finally:
        conn.close()

def ensure_tokens_table():
    """Ensure the tokens table exists in the database."""
    conn = get_auth_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            token TEXT NOT NULL,
            expires_at DATETIME NOT NULL,
            FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
        );
        """
    )
    conn.commit()
    conn.close()

def get_auth_db():
    """Ensure auth.db exists and return a database connection."""
    db_path = "data/auth.db"
    os.makedirs("data", exist_ok=True)

    create_tables_if_not_exists(db_path)  # ✅ Call helper function to create tables

    return sqlite3.connect(db_path)

def create_tables_if_not_exists(db_path):
    """Create tables if they do not exist in the database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create users table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT UNIQUE,
            is_active INTEGER DEFAULT 1
        );
        """
    )

    # Create tokens table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tokens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            token TEXT NOT NULL,
            expires_at DATETIME NOT NULL,
            FOREIGN KEY (username) REFERENCES users (username) ON DELETE CASCADE
        );
        """
    )

    conn.commit()
    conn.close()

@router.delete("/delete-account")
def soft_delete_account(current_user: dict = Depends(get_current_user)):
    """Soft-delete a user account (mark as inactive)"""
    conn = get_auth_db()
    cursor = conn.cursor()

    # Mark the account as inactive instead of deleting it
    cursor.execute(
        "UPDATE users SET is_active = 0 WHERE username = ?", (current_user["username"],)
    )
    conn.commit()
    conn.close()

    return {"message": "Account deactivated successfully"}

@router.delete("/delete-account/permanent")
def delete_account_permanently(current_user: dict = Depends(get_current_user)):
    """Permanently delete a user account (irreversible)"""
    conn = get_auth_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE username = ?", (current_user["username"],))
    conn.commit()
    conn.close()

    return {"message": "Account deleted permanently"}

@router.get("/reset-password/{token}")
def show_reset_form(token: str):
    """Verify reset token and return the username if valid"""
    conn = get_auth_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, expires_at FROM password_reset_tokens WHERE token = ?",
        (token,),
    )
    token_data = cursor.fetchone()

    if not token_data:
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid reset token")

    username, expires_at = token_data
    if datetime.utcnow() > datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S"):
        conn.close()
        raise HTTPException(status_code=400, detail="Reset token expired")

    return {"message": "Token is valid", "username": username}

@router.post("/reset-password/{token}")
def reset_password(token: str, data: PasswordResetData):
    """Reset password using a reset token."""
    conn = get_auth_db()
    cursor = conn.cursor()

    # Extract new password from request body
    new_password = data.new_password

    # Check if token is valid and not expired
    cursor.execute(
        "SELECT username, expires_at FROM password_reset_tokens WHERE token = ?",
        (token,),
    )
    token_data = cursor.fetchone()

    if not token_data:
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid reset token")

    username, expires_at = token_data

    # Fix: Handle microseconds in timestamp conversion
    if datetime.utcnow() > datetime.strptime(expires_at, "%Y-%m-%d %H:%M:%S.%f"):
        conn.close()
        raise HTTPException(status_code=400, detail="Reset token expired")

    # Validate new password
    validate_password(new_password)

    # Update user's password
    hashed_password = hash_password(new_password)
    cursor.execute(
        "UPDATE users SET password = ? WHERE username = ?", (hashed_password, username)
    )
    conn.commit()

    # Delete the used reset token
    cursor.execute("DELETE FROM password_reset_tokens WHERE token = ?", (token,))
    conn.commit()
    conn.close()

    return {"message": "Password successfully reset"}

@router.post("/request-reset")
def request_password_reset(request: PasswordResetRequest):
    """Generate a password reset token."""
    conn = get_auth_db()
    cursor = conn.cursor()

    # Extract username from request body
    username = request.username

    # Check if user exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")

    # Generate reset token
    reset_token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(minutes=15)

    # Store reset token
    cursor.execute(
        "INSERT INTO password_reset_tokens (username, token, expires_at) VALUES (?, ?, ?)",
        (username, reset_token, expires_at),
    )
    conn.commit()
    conn.close()

    return {"message": "Reset token generated", "reset_token": reset_token}

def ensure_password_reset_table():
    """Ensure password reset tokens table exists."""
    conn = get_auth_db()
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS password_reset_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        token TEXT NOT NULL,
        expires_at DATETIME NOT NULL
    );
    """
    )
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """Hash password securely using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/signup", response_model=Token)
def signup(user: User):
    """Signup user with secure password hashing."""
    conn = get_auth_db()
    cursor = conn.cursor()

    # Validate password security
    validate_password(user.password)

    # Ensure username is unique
    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Username already registered")

    # Store hashed password
    hashed_password = hash_password(user.password)
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        (user.username, hashed_password),
    )
    conn.commit()
    conn.close()

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

def validate_password(password: str):
    """Ensure password meets security standards."""
    if len(password) < 8:
        raise HTTPException(
            status_code=400, detail="Password must be at least 8 characters long."
        )
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one uppercase letter.",
        )
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one lowercase letter.",
        )
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=400, detail="Password must contain at least one number."
        )
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least one special character.",
        )

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_auth_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (form_data.username,))
    user = cursor.fetchone()

    if user:
        user = dict(zip([column[0] for column in cursor.description], user))

    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token({"sub": form_data.username})

    # Store the token in the database
    expires_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    cursor.execute(
        "INSERT INTO tokens (username, token, expires_at) VALUES (?, ?, ?)",
        (form_data.username, access_token, expires_at),
    )
    conn.commit()
    conn.close()

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username_value = payload.get("sub")

        if not isinstance(username_value, str):
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )

        username = username_value  # Remove redundant assignment

        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.put("/auth/restore-account")
def restore_account(current_user: dict = Depends(get_current_user)):
    conn = get_auth_db()
    cursor = conn.cursor()

    # Check if the user exists and is inactive
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND is_active = 0",
        (current_user["username"],),
    )
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found or already active")

    # Restore the user account
    cursor.execute(
        "UPDATE users SET is_active = 1 WHERE username = ?", (current_user["username"],)
    )
    conn.commit()
    conn.close()

    return {"message": "Account restored successfully"}
