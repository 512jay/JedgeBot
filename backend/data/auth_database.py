from dotenv import load_dotenv
import os

# Explicitly load the correct .env file
env_path = os.path.join(os.path.dirname(__file__), ".env.auth")
load_dotenv(env_path, override=True)  # Ensure it loads

# Retrieve credentials
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Now included
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Debugging: Ensure values are loaded
print(f"Loaded DB Config: {DB_NAME}, {DB_USER}, {DB_HOST}, {DB_PORT}, {DB_PASSWORD}")

# Convert DB_PORT to integer (fixes ValueError)
DB_PORT = int(DB_PORT) if DB_PORT else 5433  # Default to 5433 if missing
