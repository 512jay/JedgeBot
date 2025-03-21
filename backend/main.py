# /backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from backend.api.auth_routes import router as auth_router
from backend.api.password_reset_routes import router as password_reset_router

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"],
)

# 🔐 Authentication & Password Management
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(password_reset_router, prefix="/auth", tags=["Password Reset"])


@app.get("/")
def read_root():
    return {"message": "JedgeBot API is running!"}
