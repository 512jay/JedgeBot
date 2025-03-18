import os

import psycopg2
from dotenv import load_dotenv


def drop_and_create_database():
    """Drops the existing database and recreates it."""
    try:
        conn = psycopg2.connect(
            dbname="postgres",  # Connect to the default PostgreSQL database
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Drop the existing database if it exists
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
        print(f"Database '{DB_NAME}' dropped successfully.")

        # Create a new database
        cursor.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"Database '{DB_NAME}' created successfully.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")


def create_tables():
    """Creates the necessary authentication tables."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        cursor = conn.cursor()

        CREATE_TABLES_SQL = """
        CREATE TABLE IF NOT EXISTS users (
            user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            email VARCHAR(255) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role VARCHAR(10) CHECK (role IN ('client', 'manager')) DEFAULT 'client',
            subscription_plan VARCHAR(20) CHECK (subscription_plan IN ('free', 'paid', 'manager')),
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
        
        CREATE TABLE IF NOT EXISTS managers_clients (
            manager_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
            client_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
            PRIMARY KEY (manager_id, client_id)
        );
        
        CREATE TABLE IF NOT EXISTS client_accounts (
            account_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            client_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
            broker_name VARCHAR(50) NOT NULL,
            account_number VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
        """

        cursor.execute(CREATE_TABLES_SQL)
        conn.commit()
        print("Tables created successfully.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    load_dotenv()

    # Database connection settings
    DB_NAME = os.getenv("DB_NAME", "jedgebot_auth")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5433")

    drop_and_create_database()  # Step 1: Delete and recreate database
    create_tables()  # Step 2: Create necessary tables
