from __future__ import annotations

import json
import logging
from contextlib import suppress
from pathlib import Path

from data_farm.app.logging_config import LOGGER_NAME, setup_logging


def _flush_close(logger: logging.Logger) -> None:
    for h in logger.handlers:
        with suppress(Exception):
            h.flush()
        with suppress(Exception):
            h.close()


def test_setup_logging_console_only_adds_stderr_handler(dfarm_logger: logging.Logger) -> None:
    setup_logging(verbosity=1, log_file=None, force=True)
    logger = logging.getLogger(LOGGER_NAME)

    assert logger.handlers, "Expected at least one handler"
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers)


def test_setup_logging_idempotent_when_force_false(dfarm_logger: logging.Logger) -> None:
    setup_logging(verbosity=1, log_file=None, force=False)
    logger = logging.getLogger(LOGGER_NAME)
    first = list(logger.handlers)

    setup_logging(verbosity=2, log_file=None, force=False)
    second = list(logger.handlers)

    assert first == second, "Expected no duplicate handlers when already configured"


def test_setup_logging_force_replaces_handlers(dfarm_logger: logging.Logger) -> None:
    setup_logging(verbosity=1, log_file=None, force=True)
    logger = logging.getLogger(LOGGER_NAME)
    first = list(logger.handlers)

    setup_logging(verbosity=1, log_file=None, force=True)
    second = list(logger.handlers)

    assert len(second) >= 1

    # Ensure handlers were replaced, not reused
    assert first != second
    assert not any(h1 is h2 for h1 in first for h2 in second)


def test_setup_logging_writes_csv_and_jsonl(tmp_log_base: Path, dfarm_logger: logging.Logger) -> None:
    setup_logging(verbosity=1, log_file=str(tmp_log_base), force=True)
    logger = logging.getLogger(LOGGER_NAME)

    logger.info("Hello %s", "World")

    _flush_close(logger)

    csv_path = tmp_log_base.with_suffix(".csv")
    jsonl_path = tmp_log_base.with_suffix(".jsonl")

    assert csv_path.exists()
    assert jsonl_path.exists()

    csv_text = csv_path.read_text(encoding="utf-8")
    assert "Hello World" in csv_text

    lines = [ln for ln in jsonl_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert lines, "Expected at least one JSONL row"
    obj = json.loads(lines[-1])
    assert obj["message"] == "Hello World"
    assert obj["level"] == "INFO"
