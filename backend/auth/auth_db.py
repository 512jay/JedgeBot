# /backend/data/database/auth/auth_db.py
# Handles the setup and interaction with the authentication database using SQLAlchemy.

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.auth.models import AuthBase

# -----------------------------------------------------------------------------
# Load environment variables from .env.auth
# -----------------------------------------------------------------------------
load_dotenv()

# -----------------------------------------------------------------------------
# Build the PostgreSQL connection string
# -----------------------------------------------------------------------------
DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# -----------------------------------------------------------------------------
# Create the SQLAlchemy engine and session factory
# -----------------------------------------------------------------------------
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# -----------------------------------------------------------------------------
# Function to initialize the database (create all tables)
# -----------------------------------------------------------------------------
def init_db():
    """Create all tables defined in the authentication database schema."""
    AuthBase.metadata.create_all(bind=engine)


# -----------------------------------------------------------------------------
# Dependency function for FastAPI routes to get a DB session
# -----------------------------------------------------------------------------
def get_db():
    """
    Yields a new database session to FastAPI route handlers.

    Ensures that the session is closed after the request is completed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------------------------------------------------------
# CLI Utility: Initialize the database if run as a script
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    init_db()
    print("Authentication database setup complete.")
