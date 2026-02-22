"""
Generate and return a SQL INSERT statement.

This module generates a SQL INSERT statement based on a
list of ``ColumnEmitDefinition``s. The INSERT statement
is then returned to the calling layer.

This module does not:
- Generate the values included in the INSERT statement
- Inspect the data source to obtain column metadata used
  in value generation
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from data_farm.emitters.base import Emitter
from data_farm.models.models import ColumnEmitDefinition
from data_farm.utils.enums import SqlType


def _quote_sql_string(value: str) -> str:
    # Minimal escaping for single quotes.
    return "'" + value.replace("'", "''") + "'"


def _format_bool(value: Any) -> str:
    # Accept bool or common string inputs.
    if isinstance(value, bool):
        return "true" if value else "false"

    if isinstance(value, str):
        v = value.strip().lower()
        return "true" if v in {"true", "t", "1", "yes", "y"} else "false"

    return "true" if value else "false"


def _format_jsonb(value: Any) -> str:
    # Assume value is already valid JSON text.
    return f"'{value}'::jsonb"


_FORMATTERS: dict[SqlType, Callable[[Any], str]] = {
    SqlType.STRING: lambda v: _quote_sql_string(str(v)),
    SqlType.UUID: lambda v: _quote_sql_string(str(v)),
    SqlType.BOOLEAN: _format_bool,
    SqlType.INTEGER: lambda v: str(int(v)),
    SqlType.FLOAT: lambda v: str(float(v)),
    SqlType.DECIMAL: str,
    SqlType.DATE: str,
    SqlType.DATETIME: str,
    SqlType.JSON: _format_jsonb,
}


def get_formatter(sql_type: SqlType) -> Callable[[Any], str] | None:
    """Return the SQL literal formatter for a given SqlType, if registered."""

    return _FORMATTERS.get(sql_type)


class SqlEmitter(Emitter):
    """Emit INSERT statements."""

    def __init__(self) -> None:
        self._cols_cache: dict[tuple[str, tuple[str, ...]], str] = {}

    def emit(self, table: str, emit_defs: list[ColumnEmitDefinition]) -> Iterable[str]:
        col_names = tuple(ed.name for ed in emit_defs)
        cache_key = (table, col_names)

        cols = self._cols_cache.get(cache_key)
        if cols is None:
            cols = ", ".join(col_names)
            self._cols_cache[cache_key] = cols

        vals = build_vals(emit_defs)
        yield f"INSERT INTO {table} ({cols}) VALUES ({vals});"


def build_vals(emit_defs: list[ColumnEmitDefinition]) -> str:
    parts: list[str] = []
    append = parts.append
    for ed in emit_defs:
        fmt = _FORMATTERS.get(ed.data_type)
        append(str(ed.value) if fmt is None else fmt(ed.value))
    return ", ".join(parts)


def format_values_fast(
    values: list[Any],
    formatters: list[Callable[[Any], str] | None],
) -> str:
    """Format a row of values using a parallel list of pre-resolved formatters."""

    parts: list[str] = [""] * len(values)
    for i, v in enumerate(values):
        fmt = formatters[i]
        parts[i] = str(v) if fmt is None else fmt(v)
    return ", ".join(parts)
