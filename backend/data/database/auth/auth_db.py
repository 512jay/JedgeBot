# /backend/data/database/auth/auth_db.py
# Handles the setup and interaction with the authentication database using SQLAlchemy.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from backend.data.database.auth.models import AuthBase

# Load environment variables from .env.auth
env_path = os.path.join(os.path.dirname(__file__), ".env.auth")
load_dotenv(env_path)

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Database Engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Function to create tables
def init_db():
    """Yield a new SQLAlchemy session."""
    AuthBase.metadata.create_all(bind=engine)


# Dependency to get the DB session
def get_db():
    """Yield a new SQLAlchemy session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("Authentication database setup complete.")
