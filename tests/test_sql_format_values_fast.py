from __future__ import annotations

from typing import Any

from data_farm.emitters.sql import format_values_fast, get_formatter
from data_farm.l0_domain.enums import SqlType


def test_format_values_fast_formats_using_parallel_formatters() -> None:
    values: list[Any] = ["Alice", "42", True, "0.5"]
    formatters = [
        get_formatter(SqlType.STRING),
        get_formatter(SqlType.INTEGER),
        get_formatter(SqlType.BOOLEAN),
        get_formatter(SqlType.FLOAT),
    ]
    out = format_values_fast(values, formatters)
    assert out == "'Alice', 42, true, 0.5"
