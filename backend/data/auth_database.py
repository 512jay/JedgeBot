from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.data.auth_base import AuthBase
import os
from dotenv import load_dotenv

# Load environment variables from .env.auth
env_path = os.path.join(os.path.dirname(__file__), ".env.auth")
load_dotenv(env_path)

# Database connection settings
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create SQLAlchemy engine
auth_engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=auth_engine)


# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Bind models to metadata
AuthBase.metadata.create_all(bind=auth_engine)
