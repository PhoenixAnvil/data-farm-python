from __future__ import annotations

import logging
from pathlib import Path

from data_farm.app.logging_config import CsvFormatter, HeaderRotatingFileHandler


def test_rollover_creates_new_file(tmp_path: Path):
    fields = ["timestamp", "level", "indent_level", "module", "func", "line", "message"]
    path = tmp_path / "roll.csv"

    h = HeaderRotatingFileHandler(
        path,
        header=",".join(fields),
        maxBytes=200,
        backupCount=1,
        delay=True,
        encoding="utf-8",
    )
    h.setFormatter(CsvFormatter(fields))
    h.setLevel(logging.INFO)

    logger = logging.getLogger("dfarm.roll.test")
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger.addHandler(h)

    for _ in range(50):
        logger.info("x" * 20)

    h.flush()
    h.close()

    files = list(tmp_path.glob("roll*"))
    assert len(files) >= 1
