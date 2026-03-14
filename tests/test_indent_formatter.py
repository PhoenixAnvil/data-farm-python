from __future__ import annotations

import io
import logging

from data_farm.l2_interface_adapters.logging.logging import IndentFormatter, log_depth


# ruff: noqa: PLR0915
def test_indent_formatter_prefixes_message_only() -> None:
    stream = io.StringIO()
    h = logging.StreamHandler(stream)
    h.setFormatter(IndentFormatter("%(levelname)s %(message)s"))

    logger = logging.getLogger("dfarm.indent.test")
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger.addHandler(h)

    # no indent
    logger.info("Hello")
    # indent
    token = log_depth.set(2)
    try:
        logger.info("World")
    finally:
        log_depth.reset(token)

    h.flush()
    text = stream.getvalue().splitlines()
    assert text[0].endswith("Hello")
    assert "    World" in text[1]  # 2 levels * 2 spaces
