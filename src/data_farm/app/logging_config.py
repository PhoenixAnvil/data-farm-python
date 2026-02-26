"""Configure Data Farm logging.

Design goals:

- Console logs always go to stderr (stdout is reserved for generated data).
- File logging is enabled only when explicitly requested.
- Logs are easy to scan: start/complete markers, elapsed time, and indentation
  to reflect call hierarchy.

This module defines logging conventions and handler setup. It does not perform
application logic.
"""

from __future__ import annotations

import csv
import io
import logging
import sys
from datetime import UTC, datetime
from io import TextIOWrapper
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, TextIO

from data_farm.logging.logging import IndentFormatter, JsonlFormatter, log_depth

LOGGER_NAME = "dfarm"


def setup_logging(verbosity: int = 0, log_file: str | None = None, *, force: bool = False) -> None:
    """
    Configure application logging.

    verbosity:
        0 = WARNING (default)
        1 = INFO
        2+ = DEBUG

    force:
        If True, replace existing handlers on the dfarm logger.
        Useful for dev reruns; leave False for normal operation/testing.
    """
    level = set_level(verbosity)

    logger = logging.getLogger(LOGGER_NAME)
    logger.propagate = False  # don't double-log via root

    # Key: allow everything through the logger;
    # handlers decide what to output.
    logger.setLevel(logging.DEBUG)

    if force:
        logger.handlers.clear()
    elif logger.handlers:
        # already configured; don't duplicate handlers
        return

    console_formatter = IndentFormatter("%(asctime)s | %(levelname)-8s | %(message)s")

    logger.addHandler(setup_console_logger(level, console_formatter))

    if log_file:
        file_level = logging.INFO
        logger.addHandler(setup_csv_logger(log_file, file_level))
        logger.addHandler(setup_json_logger(log_file, file_level))


def setup_console_logger(level: int, formatter: logging.Formatter) -> logging.StreamHandler[TextIO]:
    console_handler: logging.StreamHandler[TextIO] = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    return console_handler


def setup_csv_logger(log_file: str, level: int = logging.DEBUG) -> logging.FileHandler:
    fields = ["timestamp", "level", "indent_level", "module", "func", "line", "message"]

    csv_path = Path(log_file).with_suffix(".csv")

    csv_handler = HeaderRotatingFileHandler(
        csv_path,
        header=",".join(fields),
        maxBytes=2_000_000,
        backupCount=5,
        delay=True,
        encoding="utf-8",
    )
    csv_handler.setLevel(level)
    csv_handler.setFormatter(CsvFormatter(fields))
    return csv_handler


def set_level(verbosity: int) -> int:
    INFO = 1
    DEBUG = 2

    if verbosity >= DEBUG:
        return logging.DEBUG
    if verbosity == INFO:
        return logging.INFO
    return logging.WARNING


class CsvFormatter(logging.Formatter):
    def __init__(self, fieldnames: list[str]) -> None:
        super().__init__()
        self._fieldnames = fieldnames

    @property
    def fieldnames(self) -> list[str]:
        return self._fieldnames

    def format(self, record: logging.LogRecord) -> str:
        # Make sure record.message exists (logging sets this via getMessage)
        record.message = record.getMessage()

        row: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "indent_level": log_depth.get(),
            "module": record.module,
            "func": record.funcName,
            "line": record.lineno,
            "message": f"{'  ' * log_depth.get()}{record.message}",
        }

        buf = io.StringIO()
        writer = csv.DictWriter(
            buf,
            fieldnames=self._fieldnames,
            extrasaction="ignore",
            quoting=csv.QUOTE_ALL,
        )
        writer.writerow(row)
        return buf.getvalue().rstrip("\r\n")


class HeaderRotatingFileHandler(RotatingFileHandler):
    def __init__(
        self,
        filename: str | Path,
        *,
        header: str,
        mode: str = "a",
        maxBytes: int = 0,  # NOSONAR
        backupCount: int = 0,  # NOSONAR
        encoding: str = "utf-8",
        delay: bool = True,
    ) -> None:
        self._header = header
        super().__init__(
            str(filename),
            mode=mode,
            maxBytes=maxBytes,
            backupCount=backupCount,
            encoding=encoding,
            delay=delay,
        )

        if not delay:
            # base opened the stream immediately; ensure header now
            self._ensure_header_on_stream(self.stream)

    def _ensure_header_on_stream(self, stream: TextIOWrapper[Any]) -> None:
        try:
            if stream.tell() == 0:
                stream.write(self._header)
                if not self._header.endswith("\n"):
                    stream.write("\n")
                stream.flush()
        except OSError:
            pass

    def _open(self) -> TextIOWrapper[Any]:
        stream = super()._open()
        self._ensure_header_on_stream(stream)
        return stream

    def doRollover(self) -> None:
        super().doRollover()
        # If stream is still open after rollover, ensure header for the new file.
        # If delay=True and it closes, _open() will handle header later.
        stream = getattr(self, "stream", None)
        if stream is not None:
            self._ensure_header_on_stream(stream)


def setup_csv_logging(log_path: Path) -> logging.Logger:
    logger = logging.getLogger("dfarm")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Avoid duplicate handlers if setup called multiple times
    logger.handlers.clear()

    fields = ["timestamp", "level", "indent_level", "module", "func", "line", "message"]
    header = ",".join(fields)

    csv_path = Path(log_path).with_suffix(".csv")

    handler = HeaderRotatingFileHandler(
        csv_path,
        header=header,
        maxBytes=2_000_000,  # 2 MB
        backupCount=5,
        delay=True,  # create file only when first log is emitted
        encoding="utf-8",
    )

    handler.setFormatter(CsvFormatter(fields))
    logger.addHandler(handler)
    return logger


def setup_json_logger(log_file: str, level: int = logging.INFO) -> logging.FileHandler:
    """
    JSONL file logger. Writes one JSON object per line.
    Uses RotatingFileHandler for rollover.
    """
    json_path = Path(log_file).with_suffix(".jsonl")

    h = RotatingFileHandler(
        str(json_path),
        maxBytes=2_000_000,
        backupCount=5,
        delay=True,
        encoding="utf-8",
    )
    h.setLevel(level)
    h.setFormatter(JsonlFormatter())
    return h
