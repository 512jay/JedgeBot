# /backend/data/database/authorization/initialize_auth_db.py
# Initialize and reset the authentication database by dropping and recreating it, and creating necessary tables.

import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from the correct .env.auth file
env_path = os.path.join(os.path.dirname(__file__), ".env.auth")
load_dotenv(env_path)

# Database connection settings from .env.auth
DB_NAME = os.getenv("DB_NAME", "jedgebot_auth")
DB_USER = os.getenv("DB_USER", "jedgebot_admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")


def drop_and_create_database():
    """Drops the existing authentication database and recreates it."""
    try:
        print("Connecting to the default PostgreSQL database...")
        conn = psycopg2.connect(
            dbname="postgres",  # Connect to default database first
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.autocommit = True
        cursor = conn.cursor()

        print(f"Dropping existing database '{DB_NAME}' if it exists...")
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")

        print(f"Creating new database '{DB_NAME}'...")
        cursor.execute(f"CREATE DATABASE {DB_NAME}")

        cursor.close()
        conn.close()
        print("Database reset successful.\n")

    except Exception as e:
        print(f"Error during database recreation: {e}")


def create_auth_tables():
    """Creates only authentication-related tables in the database."""
    try:
        print(f"Connecting to newly created database '{DB_NAME}'...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        cursor = conn.cursor()

        print("Creating authentication tables...")
        CREATE_AUTH_TABLES_SQL = """
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

        CREATE TABLE IF NOT EXISTS users (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            last_login TIMESTAMP DEFAULT NULL
        );
        """

        cursor.execute(CREATE_AUTH_TABLES_SQL)
        conn.commit()

        print("Authentication tables created successfully.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error during table creation: {e}")


if __name__ == "__main__":
    print("Starting authentication database setup...\n")
    drop_and_create_database()  # Step 1: Reset database
    create_auth_tables()  # Step 2: Create auth tables
    print("\nAuthentication database setup complete.")
