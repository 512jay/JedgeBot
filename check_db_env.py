import os
from dotenv import load_dotenv

load_dotenv()

print("DB_PORT:", os.getenv("DB_PORT"))
