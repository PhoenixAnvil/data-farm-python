from __future__ import annotations

import io
import logging

from data_farm.logging.logging import untimed


# ruff: noqa: PLR0915
def test_stacklevel_points_to_callsite():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    fmt = "%(filename)s:%(lineno)d:%(message)s"
    handler.setFormatter(logging.Formatter(fmt))

    logger = logging.getLogger("dfarm.stack.test")
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    # capture this exact line number
    call_line = None

    def call():
        nonlocal call_line
        call_line = __import__("inspect").currentframe().f_lineno + 1
        untimed(logger, "hello")

    call()
    handler.flush()
    output = stream.getvalue()
    assert str(call_line) in output
