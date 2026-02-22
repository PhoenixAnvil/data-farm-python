import logging
from pathlib import Path

from data_farm.app.logging_config import LOGGER_NAME, setup_logging


def test_setup_logging_is_idempotent() -> None:
    logger = logging.getLogger(LOGGER_NAME)
    logger.handlers.clear()

    setup_logging()
    first = len(logger.handlers)

    setup_logging()
    second = len(logger.handlers)

    assert first == second


def test_setup_logging_force_replaces_handlers() -> None:
    logger = logging.getLogger(LOGGER_NAME)
    logger.handlers.clear()

    setup_logging()
    setup_logging(force=True)

    assert len(logger.handlers) >= 1


def test_setup_logging_writes_file(tmp_path: Path) -> None:
    logger = logging.getLogger(LOGGER_NAME)
    logger.handlers.clear()

    log_path = tmp_path / "dfarm.log"
    setup_logging(log_file=str(log_path))

    logging.getLogger(LOGGER_NAME).info("hello")
    assert "hello" in log_path.read_text(encoding="utf-8")
