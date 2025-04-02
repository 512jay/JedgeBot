# /backend/core/settings.py
# Pydantic settings model for the FastAPI application.

import os
from dotenv import load_dotenv
from pathlib import Path

# Choose the correct .env file based on environment
# Always base everything from the root folder of your project
root_dir = (
    Path(__file__).resolve().parent.parent
)  # points to /backend's parent (i.e., project root)
backend_dir = root_dir / "backend"

env_file = backend_dir / (
    ".env.production" if os.getenv("RENDER") == "true" else ".env"
)
load_dotenv(dotenv_path=env_file, override=True)

# Optional debugging
print(f"🔧 Loaded: {env_file.name}")


from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = Field(default="development")
    TESTING: bool = Field(default=False)
    FRONTEND_URL: str = Field(default="http://localhost:5173")
    BACKEND_URL: str
    DATABASE_URL: str = Field(default="sqlite:///./auth.db")
    TASTYTRADE_USERNAME: str
    TASTYTRADE_PASSWORD: str
    TASTYTRADE_PAPER_USERNAME: str
    TASTYTRADE_PAPER_PASSWORD: str
    TASTYTRADE_ENV: str
    TASTYTRADE_DRY_RUN: bool
    LOG_LEVEL: str
    LOG_TO_CONSOLE: bool
    CHATGTP_API_KEY: str
    VITE_API_URL: str
    SECRET_KEY: str
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_FROM: str
    EMAIL_VERIFICATION_ALGORITHM: str
    ALLOW_REGISTRATION: bool = Field(default=True)
    RENDER: bool

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    print(f"🌍 ENVIRONMENT: {os.getenv('ENVIRONMENT')}, RENDER: {os.getenv('RENDER')}")
    if os.getenv("DATABASE_URL") == None:
        print("🚫 DATABASE_URL is not set!")
    else: 
        db_url: str | None = os.getenv("DATABASE_URL")
        if isinstance(db_url, str):
            masked: str = db_url.split("@")[0].split("//")[0] + "@***"
            print(f"🔐 DATABASE_URL loaded (masked): {masked}")


settings = Settings()
