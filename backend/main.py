# /backend/main.py
# Main entry point for the FastAPI backend application.

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
import os
from backend.api.auth_routes import router as auth_router
from backend.api.password_reset_routes import router as password_reset_router
from backend.core.rate_limit import limiter
from backend.core.rate_limit import limiter

TESTING = os.getenv("TESTING", "false").lower() == "true"


# Load environment variables
load_dotenv()
if os.getenv("ENVIRONMENT") == "production" and os.getenv("TESTING") == "true":
    raise RuntimeError("❌ TESTING=true in production! Rate limiting will be disabled.")

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Initialize app
app = FastAPI()
app.state.limiter = limiter

if not TESTING:
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    @app.exception_handler(RateLimitExceeded)
    async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Please wait and try again."},
        )


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"],
)

# Routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(password_reset_router, prefix="/auth", tags=["Password Reset"])
