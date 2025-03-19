from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base  # Import models if defined elsewhere

# Load the correct .env file
env_path = os.path.join(os.path.dirname(__file__), ".env.auth")
load_dotenv(env_path)

# Retrieve credentials from the environment
DB_NAME = os.getenv("AUTH_DB_NAME")
DB_USER = os.getenv("AUTH_DB_USER")
DB_PASSWORD = os.getenv("AUTH_DB_PASSWORD")
DB_HOST = os.getenv("AUTH_DB_HOST")
DB_PORT = os.getenv("AUTH_DB_PORT")

# Create the database connection
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
