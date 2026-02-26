from __future__ import annotations

import contextvars
import json
import logging
import time
from collections.abc import Mapping
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from types import TracebackType
from typing import TypeAlias


def generate_log_file_name() -> str:
    """Generate a name for the Data Farm log file."""
    return f"data_farm_{datetime.now(UTC):%Y%m%d_%H%M%S}.log"


@contextmanager
def timed(log: logging.Logger, label: str):
    # Entry
    depth = log_depth.get()
    log.info("%-4s %s", ">>>", label, stacklevel=3)

    token = log_depth.set(depth + 1)
    start = time.perf_counter()

    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        log_depth.reset(token)
        log.info("%-4s %s (%.3fs)", "<<<", label, elapsed, stacklevel=2)


ExcInfo: TypeAlias = (
    bool | BaseException | tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None] | None
)


def untimed(
    log: logging.Logger,
    msg: str,
    *args: object,
    exc_info: ExcInfo = None,
    extra: Mapping[str, object] | None = None,
    stack_info: bool = False,
    stacklevel: int = 2,
) -> None:
    log.info(
        "---  " + msg,
        *args,
        exc_info=exc_info,
        extra=extra,
        stack_info=stack_info,
        stacklevel=stacklevel,
    )


log_depth: contextvars.ContextVar[int] = contextvars.ContextVar(
    "log_depth",
    default=0,
)


class IndentFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        depth = log_depth.get()
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

        dt = datetime.fromtimestamp(record.created, tz=UTC)
        return dt.strftime("%Y-%m-%d %H:%M:%S.") + f"{int(record.msecs):03d}"


@dataclass(frozen=True)
class JsonLogRow:
    timestamp: str
    level: str
    indent_level: int
    logger: str
    module: str
    func: str
    line: int
    message: str
    exc_info: str | None = None


class JsonlFormatter(logging.Formatter):
    """Line-delimited JSON formatter (JSONL). One log record per line."""

    def format(self, record: logging.LogRecord) -> str:
        depth = log_depth.get()

        # logging's canonical message resolution
        message = record.getMessage()

        exc_text: str | None = None
        if record.exc_info:
            # Uses stdlib formatter logic to turn exc_info into text
            exc_text = self.formatException(record.exc_info)

        row = JsonLogRow(
            timestamp=datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            level=record.levelname,
            indent_level=depth,
            logger=record.name,
            module=record.module,
            func=record.funcName,
            line=record.lineno,
            message=message,
            exc_info=exc_text,
        )

        return json.dumps(asdict(row), ensure_ascii=False)
