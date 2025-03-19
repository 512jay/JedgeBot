import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from the correct .env.business file
env_path = os.path.join(os.path.dirname(__file__), ".env.business")
load_dotenv(env_path)

# Database connection settings from .env.business
DB_NAME = os.getenv("DB_NAME", "jedgebot_business")
DB_USER = os.getenv("DB_USER", "jedgebot_admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")


def drop_and_create_database():
    """Drops the existing business database and recreates it."""
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


def create_business_tables():
    """Creates business-related tables in the database."""
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

        print("Creating business tables...")
        CREATE_BUSINESS_TABLES_SQL = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            auth_user_id INTEGER UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS roles (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS user_roles (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            role_id INTEGER REFERENCES roles(id)
        );

        CREATE TABLE IF NOT EXISTS subscriptions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            plan_type VARCHAR(50) NOT NULL,
            active_until TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS broker_accounts (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            broker_name VARCHAR(100) NOT NULL,
            account_number VARCHAR(100) UNIQUE NOT NULL,
            active BOOLEAN DEFAULT TRUE
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            amount NUMERIC NOT NULL,
            currency VARCHAR(10) DEFAULT 'USD',
            status VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            manager_id INTEGER REFERENCES users(id),
            client_id INTEGER REFERENCES users(id),
            active BOOLEAN DEFAULT TRUE
        );
        """
        cursor.execute(CREATE_BUSINESS_TABLES_SQL)
        conn.commit()

        print("Business tables created successfully.")
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error during table creation: {e}")


if __name__ == "__main__":
    print("Starting business database setup...\n")
    drop_and_create_database()  # Step 1: Reset database
    create_business_tables()  # Step 2: Create business tables
    print("\nBusiness database setup complete.")
