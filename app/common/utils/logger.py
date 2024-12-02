import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from loguru import logger

LOG_FILE = "logs/election-app.log"
SENSITIVE_KEYS = {"password", "secret", "token", "api_key", "api_secret"}


def mask_sensitive_data(data):
    if isinstance(data, dict):
        return {
            key: (
                "****"
                if key.lower() in SENSITIVE_KEYS
                else mask_sensitive_data(value)
            )
            for key, value in data.items()
        }
    elif isinstance(data, list):
        return [mask_sensitive_data(item) for item in data]
    return data


def setup_standard_logging():
    file_handler = TimedRotatingFileHandler(
        LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=90,
    )
    file_handler.suffix = "%Y-%m-%d.log"
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    file_handler.setLevel(logging.INFO)

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname.upper(), record.getMessage())


def setup_loguru():
    logger.remove()
    logger.add(
        # LOG_FILE,
        "logs/{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="90 days",
        level="INFO",
        format="{time} - {level} - {message}",
        enqueue=True,
    )
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)


# setup_standard_logging()
setup_loguru()

app_logger = logger
