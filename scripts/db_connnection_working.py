# /scripts/test_db_connection.py
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv("../backend/.env.production")

db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("❌ DATABASE_URL not set.")
    exit(1)

print(f"🔌 Trying to connect to: {db_url}")

try:
    engine = create_engine(db_url)
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("✅ Connection successful:", result.scalar())
except Exception as e:
    print("❌ Connection failed:", e)
