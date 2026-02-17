import logging
import sys
from pathlib import Path


def setup_logging(verbosity: int = 0, log_file: str | None = None) -> None:
    """
    Configure application logging.

    verbosity:
        0 = WARNING (default)
        1 = INFO
        2+ = DEBUG
    """

    if verbosity >= 2:
        level = logging.DEBUG
    elif verbosity == 1:
        level = logging.INFO
    else:
        level = logging.WARNING

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Clear any existing handlers (important if re-running in dev)
    root_logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    # Console handler → stderr (Unix convention)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Optional file handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)  # file always captures full detail
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
