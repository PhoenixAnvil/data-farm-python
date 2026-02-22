"""
Configure Data Farm's logging system.

This module establishes logging behavior and conventions used
throughout the application.

Design principles:

- Logging to a file occurs only when explicitly requested.
- All console logging is written to standard error.
- Standard output remains reserved for generated data, enabling
  UNIX-style redirection and pipeline composition.

Structured logging conventions:

- Key operations are logged with Start (>>>) and Complete (<<<) markers.
- Completion markers include total execution time.
- Nested operations are indented to reflect call hierarchy.

Log levels:

- INFO: Start and completion of major operations.
- WARNING: Recoverable or potentially problematic conditions.
- DEBUG: Detailed diagnostic information for troubleshooting.

This module does not perform application logic. It defines
the logging contract and ensures consistent behavior across
the system.
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
