from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.data.auth_base import AuthBase  # Import from auth_base.py

# Load environment variables from `.env.auth`
env_path = os.path.join(os.path.dirname(__file__), ".env.auth")
load_dotenv(env_path)

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Ensure DB_PORT is properly converted to an integer
DB_PORT = int(DB_PORT) if DB_PORT else 5433

# Create database connection
AUTH_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
auth_engine = create_engine(AUTH_DATABASE_URL, echo=True)
AuthSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=auth_engine)

# Ensure tables are created (since Alembic is not being used)
AuthBase.metadata.create_all(bind=auth_engine)
