import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection settings
DB_NAME = os.getenv("DB_NAME", "jedgebot_auth")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")

# SQL commands to create tables
CREATE_TABLES_SQL = """
-- Users Table: Stores authentication details
CREATE TABLE IF NOT EXISTS users (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(10) CHECK (role IN ('client', 'manager')) DEFAULT 'client',
    subscription_plan VARCHAR(20) CHECK (subscription_plan IN ('free', 'paid', 'manager')),
    password_reset_token TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Managers-Clients Table: Many-to-many relationship between managers and clients
CREATE TABLE IF NOT EXISTS managers_clients (
    manager_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    client_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    PRIMARY KEY (manager_id, client_id)
);

-- Client Accounts Table: Each client can have multiple brokerage accounts
CREATE TABLE IF NOT EXISTS client_accounts (
    account_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID REFERENCES users(user_id) ON DELETE CASCADE,
    broker_name VARCHAR(50) NOT NULL,
    account_number VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
"""


def create_database():
    """Connects to PostgreSQL and creates the authentication database"""
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="postgres",  # Connect to the default DB first
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Create the JedgeBot Auth Database if it doesn't exist
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"Database '{DB_NAME}' created successfully.")
        else:
            print(f"Database '{DB_NAME}' already exists.")

        cursor.close()
        conn.close()

        # Connect to the newly created DB
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        cursor = conn.cursor()

        # Execute SQL to create tables
        cursor.execute(CREATE_TABLES_SQL)
        conn.commit()
        print("Tables created successfully.")

        # Close connection
        cursor.close()
        conn.close()
        print("Database setup complete.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    create_database()
