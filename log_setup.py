from loguru import logger
import os

# Define log directory and file
log_dir = "logs"
log_file = os.path.join(log_dir, "system.log")

# Ensure log directory exists
os.makedirs(log_dir, exist_ok=True)

# Define log format
log_format = (
    "[{time:YYYY-MM-DD HH:mm:ss}] {level} - {message}\n"
    "    ↳ File: {file}:{line} | Function: {function} | Process: {process} | Thread: {thread}\n"
)

# Remove existing handlers (if any) and add new ones
logger.remove()
logger.add(log_file, format=log_format, level="INFO", rotation="10 MB", compression="zip")
logger.add("logs/errors.log", format=log_format, level="ERROR", rotation="10 MB", compression="zip")
logger.add("logs/debug.log", format=log_format, level="DEBUG", rotation="10 MB", compression="zip")
logger.add("logs/trades.log", format=log_format, level="INFO", filter=lambda record: "trade" in record["message"])

logger.info("📜 Logging system initialized.")

