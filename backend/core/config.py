# /backend/core/config.py
# Centralized re-export of frequently used environment settings.

from backend.core.settings import settings

SECRET_KEY = settings.SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
EMAIL_FROM = settings.EMAIL_FROM
EMAIL_HOST = settings.EMAIL_HOST
EMAIL_PORT = settings.EMAIL_PORT
EMAIL_PASSWORD = settings.EMAIL_PASSWORD
FRONTEND_URL = settings.FRONTEND_URL
ALLOW_REGISTRATION = settings.ALLOW_REGISTRATION
DATABASE_URL = settings.DATABASE_URL
