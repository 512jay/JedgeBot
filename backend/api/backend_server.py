# /backend/api/backend_server.py
# Main entry point for the FastAPI application.

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from backend.api.auth_routes import router as auth_router
#from backend.api.clients_routes import router as clients_router
from backend.data.database.auth.auth_db import SessionLocal as AuthSession

load_dotenv()

# Set frontend URL for CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

# Initialize FastAPI app
app = FastAPI()

# ✅ CORS Configuration: Ensure Cookies Are Allowed
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # ✅ Allow frontend to access the API
    allow_credentials=True,  # ✅ Allow credentials (cookies)
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],  # ✅ Headers frontend can send
    expose_headers=["Set-Cookie"],  # ✅ Expose "Set-Cookie" so frontend sees cookies
)

# ✅ Register API Routes
app.include_router(auth_router, prefix="/auth")
#app.include_router(clients_router, prefix="/clients", tags=["clients"])


# ✅ Root route to confirm API is running
@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}
