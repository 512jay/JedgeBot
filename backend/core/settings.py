# /backend/core/settings.py
# Pydantic settings model for the FastAPI application.

import os
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
    # email settings
    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_FROM: str
    EMAIL_PASSWORD: str
    ALLOW_REGISTRATION: bool = Field(default=True)
    RENDER: bool

    # token stuff
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

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
