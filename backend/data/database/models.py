# /backend/data/database/models.py

# Import all models that use the shared Base
from backend.auth.auth_models import User
from backend.user.user_models import UserProfile
from backend.auth.password.models import PasswordResetToken

from backend.data.database.base import Base

# This ensures Base.metadata reflects all models
__all__ = ["Base", "User", "UserProfile", "PasswordResetToken"]
