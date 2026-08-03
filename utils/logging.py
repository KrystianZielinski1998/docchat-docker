import sys
from pathlib import Path

from loguru import logger

# Create logger file
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Remove the default folder
logger.remove()

# 1. Logs for console
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    level="INFO",
    colorize=True,
)

# 2. Main logs file for all log types
logger.add(
    log_dir / "app_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="30 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
    level="DEBUG",
    compression="zip",
)

# 3. Seperate log file for errors
logger.add(
    log_dir / "errors_{time:YYYY-MM-DD}.log",
    rotation="1 week",
    retention="90 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {message}",
    level="ERROR",
    compression="zip",
)

# 4. JSON format for log analysis
logger.add(
    log_dir / "structured_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="14 days",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}",
    serialize=True,
    level="INFO",
)

# Export logger
__all__ = ["logger"]
