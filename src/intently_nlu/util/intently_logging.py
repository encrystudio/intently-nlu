"""Internal logging utilities"""

import logging
import os
import sys
import traceback
from enum import Enum

from platformdirs import user_log_dir


class LogLevel(Enum):
    """Log levels"""

    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


class ColoredFormatter(logging.Formatter):
    """Add color to the log messages"""

    COLORS = {
        logging.DEBUG: "\033[94m",  # Blue
        logging.INFO: "\033[92m",  # Green
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[95m",  # Magenta
    }
    RESET = "\033[0m"  # Reset color (White)

    def format(self, record: logging.LogRecord) -> str:
        log_msg = super(ColoredFormatter, self).format(record)
        color = self.COLORS.get(record.levelno, self.RESET)
        return f"{color}{log_msg}{self.RESET}"


def get_log_file() -> str:
    """Searches for a location for the log file, creates it if not exists, and returns

    Returns:
        str: Log file path.
    """
    log_file_path = user_log_dir(appname="intently-nlu", appauthor="encrystudio")
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)
    log_file_path = os.path.join(log_file_path, "intently-nlu.log")
    return log_file_path


def get_logger(name: str) -> logging.Logger:
    """Build a logger with log file and colored output

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Ready-to-use logger.
    """
    logger = logging.getLogger(name=f"{name}::")
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler(get_log_file())
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s @ %(name)s: %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.getLogger().level)
    console_formatter = ColoredFormatter("%(levelname)s @ %(name)s: %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    logger.debug("Log file is stored @ %s", get_log_file())

    return logger


def initialize_session(log_level: LogLevel) -> None:
    """Initializes new logging session

    Args:
        log_level (LogLevel): The session's log level.
    """
    logging.basicConfig(level=log_level.value, handlers=[], force=True)
    logging.getLogger().setLevel(log_level.value)
    get_logger("Session").debug("++++++++++++++ NEW SESSION INITIALIZED ++++++++++++++")


log_level_cli_map = {
    0: LogLevel.DEBUG,
    1: LogLevel.INFO,
    2: LogLevel.WARNING,
    3: LogLevel.ERROR,
    4: LogLevel.CRITICAL,
}


def log_error(logger: logging.Logger, error: Exception, action: str) -> Exception:
    """Pretty print error in logger

    Args:
        logger (logging.Logger): Logger to log the error in.
        error (Exception): The error that occurred.
        action (str): The action where the error occurred.
    Returns:
       Exception: The same error that was passed in
    """
    message = ""
    message += f"\n[ERROR] An error occurred during the action: '{action}'"
    message += f"\n  Error Type: {type(error).__name__}"
    message += f"\n  Error Message: {error}"

    message += "\n\n  Stack Trace:"
    message += "\n".join(traceback.format_tb(error.__traceback__))
    logger.error(message)
    return error
