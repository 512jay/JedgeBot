# /backend/data/database/db.py
# Handles the setup and connection to the main PostgreSQL database used by all services.
# It also provides a dependency for FastAPI routes to inject a database session.

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.data.database.base import Base  # Shared base for all models

# -----------------------------------------------------------------------------
# Load environment variables
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
# Initialize all tables if run directly (Dev only)
# -----------------------------------------------------------------------------
def init_db():
    """Create all tables registered with Base metadata."""
    Base.metadata.create_all(bind=engine)


# -----------------------------------------------------------------------------
# Dependency for FastAPI routes
# -----------------------------------------------------------------------------
def get_db():
    """
    Dependency injection for database session.

    Yields a session and ensures it's closed afterward.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------------------------------------------------------
# CLI: Run `python db.py` to create all tables
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    init_db()
    print("Database setup complete.")

# /backend/data/database/db.py
# Compare this snippet from backend/data/database/models.py: