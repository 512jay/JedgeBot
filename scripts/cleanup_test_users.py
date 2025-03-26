# scripts/cleanup_test_users.py

from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

with engine.begin() as conn:
    conn.execute(
        text(
            "DELETE FROM users WHERE email ILIKE 'test%@example.com' OR email ILIKE 'token_test_%@example.com' OR email ILIKE 'reset_test_%@example.com'"
        )
    )
    print("✅ Test users deleted.")
