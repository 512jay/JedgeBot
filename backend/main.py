# /backend/main.py
# Main entry point for the FastAPI backend application.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from backend.api.auth_routes import router as auth_router
from backend.api.password_reset_routes import router as password_reset_router

# from backend.api.clients_routes import router as clients_router  # (enable later)

# Load environment variables
load_dotenv()

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
print(FRONTEND_URL)  # Debug: Check the loaded FRONTEND_URL

# -----------------------------------------------------------------------------
# Initialize FastAPI app
# -----------------------------------------------------------------------------
app = FastAPI()

# -----------------------------------------------------------------------------
# CORS Configuration
# -----------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["Set-Cookie"],
)

# -----------------------------------------------------------------------------
# API Routes
# -----------------------------------------------------------------------------
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(password_reset_router, prefix="", tags=["Password Reset"])
# app.include_router(clients_router, prefix="/clients", tags=["Clients"])  # Optional


# -----------------------------------------------------------------------------
# Root Route
# -----------------------------------------------------------------------------
@app.get("/")
def read_root():
    return {"message": "JedgeBot API is running!"}
