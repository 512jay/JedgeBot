from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.data.database.market.trading_base import TradingBase  # Import the correct base

# Load env file for trading database
env_path = os.path.join(os.path.dirname(__file__), ".env.trading")
load_dotenv(env_path)

DB_NAME = os.getenv("TRADING_DB_NAME")
DB_USER = os.getenv("TRADING_DB_USER")
DB_PASSWORD = os.getenv("TRADING_DB_PASSWORD")
DB_HOST = os.getenv("TRADING_DB_HOST")
DB_PORT = os.getenv("TRADING_DB_PORT")

# Create separate engine and session
TRADING_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
trading_engine = create_engine(TRADING_DATABASE_URL, echo=True)
TradingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=trading_engine
)
