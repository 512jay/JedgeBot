from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from backend.api.auth import router as auth_router  

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

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}
