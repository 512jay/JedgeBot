# /scripts/alembic_helpers.py
# Script-based Alembic helpers to apply migrations with correct environment settings.

import os
import subprocess
from pathlib import Path


def run_local_migration() -> None:
    """Run Alembic upgrade using local .env file"""
    print("🏗️  Running local migration with .env...")
    env_path = Path("backend/.env")
    if not env_path.exists():
        print("❌ .env file not found.")
        return

    os.environ["DOTENV_FILE"] = str(env_path)
    result = subprocess.run(
        ["alembic", "upgrade", "head"], capture_output=True, text=True
    )

    print(result.stdout)
    if result.stderr:
        print("⚠️ STDERR:")
        print(result.stderr)


def run_remote_migration() -> None:
    """Run Alembic upgrade using .env.production file (Render DB)"""
    print("🚀 Running production migration with .env.production...")
    env_path = Path("backend/.env.production")
    if not env_path.exists():
        print("❌ .env.production file not found.")
        return

    os.environ["DOTENV_FILE"] = str(env_path)
    result = subprocess.run(
        ["alembic", "upgrade", "head"], capture_output=True, text=True
    )

    print(result.stdout)
    if result.stderr:
        print("⚠️ STDERR:")
        print(result.stderr)
