# /backend/scripts/preflight.py
# Sanity check for FastAPI backend startup and environment config

import os
import sys
# /backend/scripts/preflight.py

from dotenv import load_dotenv
import os

# 👇 This must be first to ensure .env values are in place before Pydantic runs
env_path = os.path.join(os.path.dirname(__file__), "..", ".env.production")
load_dotenv(dotenv_path=env_path, override=True)

# now you can import settings, FastAPI app, etc.

from fastapi.testclient import TestClient
from backend.main import app
from backend.core.config import DATABASE_URL, SECRET_KEY

client = TestClient(app)


def check_env_vars():
    assert SECRET_KEY, "❌ SECRET_KEY is not set!"
    assert DATABASE_URL, "❌ DATABASE_URL is not set!"
    print("✅ Environment variables look good")


def check_routes():
    response = client.get("/ping")
    assert response.status_code == 200, "❌ /ping route did not return 200"
    print("✅ Route /ping responded successfully")


def run_preflight():
    print("🚀 Running backend preflight check...")
    check_env_vars()
    check_routes()
    print("✅ Backend passed preflight checks.\n")


if __name__ == "__main__":
    try:
        run_preflight()
    except AssertionError as e:
        print(e)
        sys.exit(1)
