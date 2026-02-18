import logging
import sys
from pathlib import Path
from typing import TextIO


def setup_logging(verbosity: int = 0, log_file: str | None = None) -> None:
    """
    Configure application logging.

    verbosity:
        0 = WARNING (default)
        1 = INFO
        2+ = DEBUG
    """

    level = set_level(verbosity)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear any existing handlers (important if re-running in dev)
    root_logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    # Console handler → stderr (Unix convention)
    root_logger.addHandler(setup_console_logger(level, formatter))

    # Optional file handler
    if log_file:
        root_logger.addHandler(setup_file_logger(log_file, formatter))


def setup_console_logger(level: int, formatter: logging.Formatter) -> logging.StreamHandler[TextIO]:
    console_handler: logging.StreamHandler[TextIO] = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    return console_handler


def setup_file_logger(log_file: str, formatter: logging.Formatter) -> logging.FileHandler:
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)  # file always captures full detail
    file_handler.setFormatter(formatter)
    return file_handler


def set_level(verbosity: int) -> int:
    INFO = 1
    DEBUG = 2

    if verbosity >= DEBUG:
        return logging.DEBUG
    elif verbosity == INFO:
        return logging.INFO
    else:
        return logging.WARNING
