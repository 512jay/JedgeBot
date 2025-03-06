from loguru import logger
import os
import sys

# Define log directory and ensure it exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Define log format
LOG_FORMAT = (
    "[{time:YYYY-MM-DD HH:mm:ss}] {level} - {message}\n"
    "    ↳ File: {file}:{line} | Function: {function} | Process: {process} | Thread: {thread}\n"
)

# Get log level from environment (default to INFO)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Control console logging (default: ON in development, OFF in production)
LOG_TO_CONSOLE = os.getenv("LOG_TO_CONSOLE", "True").lower() == "true"

# Remove existing handlers to prevent duplicate logs
logger.remove()

# Console Logging (Enabled based on environment)
if LOG_TO_CONSOLE:
    logger.add(
        sys.stdout,
        format="[{time:HH:mm:ss}] <lvl>{level}</lvl> - {message}",
        level=LOG_LEVEL,
        colorize=True
    )

# File Logging (System Logs)
logger.add(
    os.path.join(LOG_DIR, "system.log"),
    format=LOG_FORMAT,
    level="INFO",
    rotation="50 MB",
    compression="zip",
)

# Error Logs (Only logs errors & critical issues)
logger.add(
    os.path.join(LOG_DIR, "errors.log"),
    format=LOG_FORMAT,
    level="ERROR",
    rotation="50 MB",
    compression="zip",
)

# Debug Logs (Only logs debug messages)
logger.add(
    os.path.join(LOG_DIR, "debug.log"),
    format=LOG_FORMAT,
    level="DEBUG",
    rotation="50 MB",
    compression="zip",
)

# Trade-Specific Logs (Filters messages containing 'trade')
logger.add(
    os.path.join(LOG_DIR, "trades.log"),
    format=LOG_FORMAT,
    level="INFO",
    rotation="50 MB",
    compression="zip",
    filter=lambda record: "trade" in record["message"]
)

# Capture uncaught exceptions
def log_exceptions(exc_type, exc_value, exc_traceback):
    """Global exception handler for logging uncaught errors."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Unhandled Exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = log_exceptions

logger.info("📜 Logging system initialized (Level: {level}, Console Logging: {console})", level=LOG_LEVEL, console=LOG_TO_CONSOLE)
