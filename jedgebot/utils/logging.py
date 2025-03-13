import os
import sys
import toml
from loguru import logger
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define default logging configuration
DEFAULT_CONFIG = {
    "log_dir": "logs",
    "global_log_level": "INFO",
    "rotation": {"size": "50 MB"},
    "retention": {"days": 30},
    "files": {},
}

# Load logging config from config.toml, falling back to default if missing
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.toml")
try:
    config = toml.load(CONFIG_PATH).get("logging", DEFAULT_CONFIG)
except (FileNotFoundError, KeyError):
    config = DEFAULT_CONFIG

LOG_DIR = config.get("log_dir", "logs")
LOG_RETENTION = f"{config['retention']['days']} days"
LOG_ROTATION = config["rotation"]["size"]

# Get log level from environment (default to INFO)
GLOBAL_LOG_LEVEL = os.getenv(
    "LOG_LEVEL", config.get("global_log_level", "INFO")
).upper()

# Check for Debug Mode from environment
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"

# Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Improved log format for readability
LOG_FORMAT = (
    "[{time:YYYY-MM-DD HH:mm:ss}] [{level}] {message} " "({file}:{line} in {function})"
)

# Remove existing handlers to prevent duplicate logs
logger.remove()

# Console Logging (Enabled based on environment)
LOG_TO_CONSOLE = os.getenv("LOG_TO_CONSOLE", "True").lower() == "true"
if LOG_TO_CONSOLE:
    logger.add(
        sys.stdout,
        format="[{time:HH:mm:ss}] <lvl>{level}</lvl> - {message}",
        level=GLOBAL_LOG_LEVEL,
        colorize=True,
    )

# System Logs (General logs)
logger.add(
    os.path.join(LOG_DIR, "system.log"),
    format=LOG_FORMAT,
    level=GLOBAL_LOG_LEVEL,
    rotation=LOG_ROTATION,
    compression="zip",
)

# Error Logs (Only logs errors & critical issues)
logger.add(
    os.path.join(LOG_DIR, "errors.log"),
    format=LOG_FORMAT,
    level="ERROR",
    rotation=LOG_ROTATION,
    compression="zip",
)

# Debug Logs (Only logs debug messages, enabled via DEBUG_MODE)
if DEBUG_MODE:
    logger.add(
        os.path.join(LOG_DIR, "debug.log"),
        format=LOG_FORMAT,
        level="DEBUG",
        rotation=LOG_ROTATION,
        compression="zip",
    )

# Trade-Specific Logs (Filters messages containing 'trade')
logger.add(
    os.path.join(LOG_DIR, "trades.log"),
    format=LOG_FORMAT,
    level="INFO",
    rotation=LOG_ROTATION,
    compression="zip",
    filter=lambda record: "trade" in record["message"],
)


# Function to create module-specific loggers
def setup_logger(log_name: str):
    """Setup a logger for a specific module (e.g., TastyTrade, IBKR, system logs)."""
    log_file = os.path.join(LOG_DIR, config["files"].get(log_name, "system.log"))
    logger.add(
        log_file,
        rotation=LOG_ROTATION,
        retention=LOG_RETENTION,
        level=GLOBAL_LOG_LEVEL,
    )
    logger.info(f"Logger initialized for {log_name} at level {GLOBAL_LOG_LEVEL}")
    return logger


# Capture uncaught exceptions globally
def log_exceptions(exc_type, exc_value, exc_traceback):
    """Global exception handler for logging uncaught errors."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Unhandled Exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = log_exceptions

logger.info(
    "📜 Logging system initialized (Level: {level}, Console Logging: {console}, Debug Mode: {debug})",
    level=GLOBAL_LOG_LEVEL,
    console=LOG_TO_CONSOLE,
    debug=DEBUG_MODE,
)
