import contextvars
import logging
import time
from collections.abc import Mapping
from contextlib import contextmanager
from types import TracebackType
from typing import TypeAlias

log_depth: contextvars.ContextVar[int] = contextvars.ContextVar(
    "log_depth",
    default=0,
)


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
