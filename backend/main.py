# /backend/main.py
# Main entry point for the FastAPI backend application.

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from backend.core.settings import settings
from backend.core.rate_limit import limiter
from backend.auth.auth_routes import router as auth_router
from backend.user.user_routes import router as user_router
from backend.auth.password_reset.routes import router as password_reset_router
from backend.core.settings import settings


# Optional safety net
if settings.ENVIRONMENT == "production" and settings.TESTING:
    raise RuntimeError("❌ TESTING=true in production! Rate limiting will be disabled.")

# Initialize FastAPI app
app = FastAPI()

if settings.TESTING:
    from backend.api import dev_routes

    app.include_router(dev_routes.router)    
# Only enable rate limiting if not in test mode
if not settings.TESTING:
    app.state.limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Please wait and try again."},
        )


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"],
)
print("🌐 CORS allowed origins:", settings.FRONTEND_URL)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(password_reset_router, prefix="/auth", tags=["Password Reset"])
app.include_router(user_router, prefix="/users", tags=["User Profiles"])
