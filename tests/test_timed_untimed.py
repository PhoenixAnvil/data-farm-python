from __future__ import annotations

import logging
from contextlib import suppress
from pathlib import Path

from data_farm.app.logging_config import LOGGER_NAME, setup_logging
from data_farm.logging.logging import log_depth, timed, untimed


def test_timed_increments_and_restores_depth(tmp_path: Path, dfarm_logger: logging.Logger) -> None:
    setup_logging(verbosity=2, log_file=str(tmp_path / "dfarm.log"), force=True)
    logger = logging.getLogger(LOGGER_NAME)
    LOG_DEPTH = 2
    assert log_depth.get() == 0
    with timed(logger, "outer"):
        assert log_depth.get() == 1
        with timed(logger, "inner"):
            assert log_depth.get() == LOG_DEPTH
        assert log_depth.get() == 1
    assert log_depth.get() == 0


def test_untimed_writes_message(tmp_path: Path, dfarm_logger: logging.Logger) -> None:
    base = tmp_path / "dfarm.log"
    setup_logging(verbosity=1, log_file=str(base), force=True)
    logger = logging.getLogger(LOGGER_NAME)

    untimed(logger, "Hello %s", "there")
    for h in logger.handlers:
        with suppress(Exception):
            h.flush()

    csv_path = base.with_suffix(".csv")
    assert "Hello there" in csv_path.read_text(encoding="utf-8")
