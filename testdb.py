import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database connection parameters
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_port = os.getenv("DB_PORT")

# Print the values being used (excluding the password for security)
print("\n🔍 **Database Connection Debug Info**")
print(f"   - DB_HOST: {db_host}")
print(f"   - DB_PORT: {db_port}")
print(f"   - DB_NAME: {db_name}")
print(f"   - DB_USER: {db_user}")
print("   - DB_PASSWORD: ****** (hidden for security)\n")

# Attempt connection
try:
    print(f"🚀 Attempting connection to {db_host}:{db_port} ...")
    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        connect_timeout=3,
    )
    print("✅ Successfully connected to the database!")
    conn.close()
except psycopg2.OperationalError as e:
    print(f"❌ Database connection failed: {e}")
