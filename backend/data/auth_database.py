from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.data.auth_base import AuthBase  # Import the correct base

# Load env file for auth database
env_path = os.path.join(os.path.dirname(__file__), ".env.auth")
load_dotenv(env_path)

DB_NAME = os.getenv("AUTH_DB_NAME")
DB_USER = os.getenv("AUTH_DB_USER")
DB_PASSWORD = os.getenv("AUTH_DB_PASSWORD")
DB_HOST = os.getenv("AUTH_DB_HOST")
DB_PORT = os.getenv("AUTH_DB_PORT")

# Create separate engine and session
AUTH_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
auth_engine = create_engine(AUTH_DATABASE_URL, echo=True)
AuthSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=auth_engine)
