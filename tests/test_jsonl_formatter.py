from __future__ import annotations

import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from data_farm.l2_interface_adapters.logging.logging import JsonlFormatter


# ruff: noqa: PLR0915
def test_jsonl_formatter_emits_one_object_per_line(tmp_path: Path) -> None:
    path = tmp_path / "x.jsonl"
    h = RotatingFileHandler(str(path), maxBytes=10_000, backupCount=1, delay=True, encoding="utf-8")
    h.setLevel(logging.INFO)
    h.setFormatter(JsonlFormatter())

    logger = logging.getLogger("dfarm.jsonl.test")
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger.addHandler(h)

    logger.info("Hello %s", "JSONL")
    h.flush()
    h.close()

    lines = path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    obj = json.loads(lines[0])
    assert obj["message"] == "Hello JSONL"
    assert obj["logger"] == "dfarm.jsonl.test"
