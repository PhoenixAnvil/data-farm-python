import json
import logging
from pathlib import Path

from data_farm.l2_interface_adapters.logging.logging_config import LOGGER_NAME, setup_logging


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

    log_path = tmp_path / "dfarm.csv"
    setup_logging(verbosity=1, log_file=str(log_path), force=True)  # INFO

    msg = "Test"
    logger.info(msg)

    # flush to be safe on Windows
    for h in logger.handlers:
        if hasattr(h, "flush"):
            h.flush()

    assert log_path.exists()
    assert msg in log_path.read_text(encoding="utf-8")


def test_setup_logging_writes_jsonl(tmp_path: Path) -> None:
    log_file = tmp_path / "dfarm.jsonl"

    setup_logging(verbosity=1, log_file=str(log_file), force=True)  # INFO
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("Hello %s", "JSON")

    # flush/close to be safe on Windows
    for h in logger.handlers:
        if hasattr(h, "flush"):
            h.flush()
        if hasattr(h, "close"):
            h.close()

    jsonl_path = log_file.with_suffix(".jsonl")
    text = jsonl_path.read_text(encoding="utf-8").strip()
    assert text

    obj = json.loads(text.splitlines()[-1])
    assert obj["message"] == "Hello JSON"
    assert obj["indent_level"] >= 0
