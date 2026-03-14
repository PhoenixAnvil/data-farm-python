from __future__ import annotations

import logging
from pathlib import Path

from data_farm.l2_interface_adapters.logging.logging_config import CsvFormatter, HeaderRotatingFileHandler


# ruff: noqa: PLR0915
def test_header_written_on_first_emit(tmp_path: Path) -> None:
    fields = ["timestamp", "level", "indent_level", "module", "func", "line", "message"]
    path = tmp_path / "x.csv"
    h = HeaderRotatingFileHandler(
        path,
        header=",".join(fields),
        maxBytes=10_000,
        backupCount=1,
        delay=True,
        encoding="utf-8",
    )
    h.setFormatter(CsvFormatter(fields))
    h.setLevel(logging.INFO)

    logger = logging.getLogger("dfarm.header.test")
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger.addHandler(h)

    logger.info("Test")
    h.flush()
    h.close()

    text = path.read_text(encoding="utf-8").splitlines()
    assert text, "Expected file to be created and non-empty"
    assert text[0] == ",".join(fields), "Expected CSV header as first line"
