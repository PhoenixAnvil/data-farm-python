import contextvars
import logging
import time
from contextlib import contextmanager
from datetime import UTC, datetime


def generate_log_file_name() -> str:
    """Generate a name for the Data Farm log file."""
    return f"data_farm_{datetime.now(UTC):%Y%m%d_%H%M%S}.log"


@contextmanager
def timed(log: logging.Logger, label: str):
    # Entry
    depth = _log_depth.get()
    log.info("%-8s %s", ">>>", label, stacklevel=3)

    token = _log_depth.set(depth + 1)
    start = time.perf_counter()

    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        _log_depth.reset(token)
        log.info("%-8s %s (%.3fs)", "<<<", label, elapsed, stacklevel=3)


_log_depth: contextvars.ContextVar[int] = contextvars.ContextVar(
    "log_depth",
    default=0,
)


class IndentFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        depth = _log_depth.get()
        indent = "  " * depth

        original_msg = record.msg
        try:
            # Only indent the message portion
            record.msg = f"{indent}{original_msg}"
            return super().format(record)
        finally:
            record.msg = original_msg

    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        if datefmt is not None:
            return super().formatTime(record, datefmt)

        dt = datetime.fromtimestamp(record.created)
        return dt.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(record.msecs):03d}"
