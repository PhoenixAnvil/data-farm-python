from __future__ import annotations

import logging


def test_indent_filter_injects_attributes():
    class DummyFilter(logging.Filter):
        def filter(self, record: logging.LogRecord):
            record.indent_level = 3
            return True

    logger = logging.getLogger("dfarm.filter.test")
    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.addFilter(DummyFilter())
    logger.addHandler(handler)

    logger.info("ok")
    # if no AttributeError, filter injection works
