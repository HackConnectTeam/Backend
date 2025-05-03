from loguru import logger

from src.backend.config.config import settings

if __name__ == "__main__":
    # Show the logger possibilities
    logger.info("This is a template for a Python project.")
    logger.error("This is an error message.")
    logger.warning("This is a warning message.")
    logger.debug("This is a debug message.")

    # Try to read values from the config file
    db = settings.db.user

    logger.info(f"Database user: {db}")
