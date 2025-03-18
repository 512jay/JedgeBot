from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from backend.api.auth import router as auth_router  
from backend.api.clients import router as clients_router  # ✅ Import clients API

# Load .env variables
load_dotenv()
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

app = FastAPI()

# Allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])  
app.include_router(
    clients_router, prefix="/clients", tags=["clients"]
)  # ✅ Add clients router

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}
