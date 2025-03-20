# /backend/api/backend_server.py
# Main entry point for the FastAPI application.
# It includes all routes

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from backend.api.auth_routes import router as auth_router
from backend.api.clients_routes import router as clients_router
from backend.data.database.authorization.auth_db import SessionLocal as AuthSession

load_dotenv()

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

app = FastAPI()

# ✅ Fix: Allow specific frontend for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],  # ✅ Allow frontend to access the API
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "DELETE",
        "OPTIONS",
    ],  # ✅ Limit allowed methods
    allow_headers=["Authorization", "Content-Type"],  # ✅ Restrict headers
)

app.include_router(auth_router, prefix="/auth")
app.include_router(clients_router, prefix="/clients", tags=["clients"])


@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}
