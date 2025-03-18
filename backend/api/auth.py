import os
import psycopg2
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional
from backend.utils.security import hash_password, verify_password, validate_password
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DB_NAME = os.getenv("DB_NAME", "jedgebot_auth")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # ✅ Load from .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
router = APIRouter()


class User(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


def get_db_connection():
    """Establishes a connection to PostgreSQL."""
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generates a JWT token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/signup", response_model=Token)
def signup(user: User):
    """Registers a new user with hashed password."""
    validate_password(user.password)  # Enforce strong passwords
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if email is already registered
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    # Insert new user into database
    cursor.execute(
        "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
        (user.email, hashed_password),
    )
    conn.commit()
    conn.close()

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticates user and returns a JWT token."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password_hash FROM users WHERE email = %s", (form_data.username,)
    )
    user = cursor.fetchone()
    conn.close()

    if not user or not verify_password(form_data.password, user[0]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token({"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    """Returns the currently logged-in user."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials"
            )
        return {"email": email}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
