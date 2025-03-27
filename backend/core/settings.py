# /backend/core/settings.py
# Pydantic settings model for the FastAPI application.
import os
from dotenv import load_dotenv

load_dotenv()  # ✅ loads .env before Pydantic tries to validate

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

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
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_FROM: str
    EMAIL_VERIFICATION_ALGORITHM: str


settings = Settings()
