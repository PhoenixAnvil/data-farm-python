"""Configure Data Farm logging.

Design goals:

- Console logs always go to stderr (stdout is reserved for generated data).
- File logging is enabled only when explicitly requested.
- Logs are easy to scan: start/complete markers, elapsed time, and indentation
  to reflect call hierarchy.

This module defines logging conventions and handler setup. It does not perform
application logic.
"""

import logging
import sys
from pathlib import Path
from typing import TextIO

from data_farm.logging.logging import IndentFormatter

LOGGER_NAME = "dfarm"


def setup_logging(verbosity: int = 0, log_file: str | None = None, *, force: bool = False) -> None:
    """
    Configure application logging.

    verbosity:
        0 = WARNING (default)
        1 = INFO
        2+ = DEBUG

    force:
        If True, replace existing handlers on the dfarm logger.
        Useful for dev reruns; leave False for normal operation/testing.
    """
    level = set_level(verbosity)

    logger = logging.getLogger(LOGGER_NAME)
    logger.propagate = False  # don't double-log via root

    # Key: allow everything through the logger;
    # handlers decide what to output.
    logger.setLevel(logging.DEBUG)

    if force:
        logger.handlers.clear()
    elif logger.handlers:
        # already configured; don't duplicate handlers
        return

    console_formatter = IndentFormatter("%(asctime)s | %(levelname)-8s | %(message)s")

    file_formatter = IndentFormatter("%(asctime)s | %(levelname)-8s | %(module)s:%(funcName)s:%(lineno)d | %(message)s")

    logger.addHandler(setup_console_logger(level, console_formatter))

    if log_file:
        logger.addHandler(setup_file_logger(log_file, file_formatter))


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
    if verbosity == INFO:
        return logging.INFO
    return logging.WARNING
