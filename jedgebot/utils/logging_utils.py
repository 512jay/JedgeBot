import os
import toml
from loguru import logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load logging config from config.toml
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.toml")
config = toml.load(CONFIG_PATH)["logging"]

LOG_DIR = config.get("log_dir", "logs")
LOG_RETENTION = f"{config['retention']['days']} days"
LOG_ROTATION = config["rotation"]["size"]

# Check environment variable for log level, fallback to config.toml
GLOBAL_LOG_LEVEL = os.getenv("LOG_LEVEL", config.get("global_log_level", "INFO"))

# Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(log_name: str):
    """Setup a logger for a specific module (e.g., TastyTrade, IBKR, system logs)."""
    log_file = os.path.join(LOG_DIR, config["files"].get(log_name, "system.log"))
    logger.add(log_file, rotation=LOG_ROTATION, retention=LOG_RETENTION, level=GLOBAL_LOG_LEVEL)
    logger.info(f"Logger initialized for {log_name} at level {GLOBAL_LOG_LEVEL}")
    return logger
