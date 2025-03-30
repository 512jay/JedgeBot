# /run_maintenance.py
# Script to run periodic maintenance tasks like cleanup of expired or used data.

from backend.data.database.db import get_db
from backend.dev.cleanup import cleanup_password_reset_tokens


def run():
    print("🧹 Running maintenance tasks...")

    db_gen = get_db()
    db = next(db_gen)
    try:
        deleted = cleanup_password_reset_tokens(db)
        print(f"✅ Deleted {deleted} used/expired password reset tokens.")
    finally:
        db.close()

    print("✅ All maintenance tasks complete.")


if __name__ == "__main__":
    run()
