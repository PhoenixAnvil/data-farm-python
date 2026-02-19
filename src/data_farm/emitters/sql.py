from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from data_farm.emitters.base import Emitter
from data_farm.models.models import ColumnEmitDefinition
from data_farm.utils.enums import SqlType


def _quote_sql_string(value: str) -> str:
    # Minimal escaping for single quotes
    return "'" + value.replace("'", "''") + "'"


def _format_bool(value: Any) -> str:
    # Accept bool or common string inputs
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        v = value.strip().lower()
        return "true" if v in {"true", "t", "1", "yes", "y"} else "false"
    return "true" if value else "false"


def _format_json(value: str) -> str:
    return f"'{value}'::jsonb"


_FORMATTERS: dict[SqlType, Callable[[Any], str]] = {
    SqlType.STRING: lambda v: _quote_sql_string(str(v)),
    SqlType.UUID: lambda v: _quote_sql_string(str(v)),
    SqlType.BOOLEAN: _format_bool,
    SqlType.INTEGER: lambda v: str(int(v)),
    SqlType.FLOAT: lambda v: str(float(v)),
    SqlType.DECIMAL: lambda v: str(v),
    SqlType.DATE: lambda v: str(v),
    SqlType.DATETIME: lambda v: str(v),
    SqlType.JSON: lambda v: str(_format_json(v)),
}


class SqlEmitter(Emitter):
    """Emit INSERT statements efficiently."""

    def __init__(self) -> None:
        # Cache computed "col1, col2, col3" strings by (table, column-names)
        self._cols_cache: dict[tuple[str, tuple[str, ...]], str] = {}

    def emit(self, table: str, emit_defs: list[ColumnEmitDefinition]) -> Iterable[str]:
        # Column names are stable per table schema; compute once per (table, column order)
        col_names = tuple(ed.name for ed in emit_defs)
        cache_key = (table, col_names)

        cols = self._cols_cache.get(cache_key)
        if cols is None:
            cols = ", ".join(col_names)
            self._cols_cache[cache_key] = cols

        vals = build_vals(emit_defs=emit_defs)
        yield f"INSERT INTO {table} ({cols}) VALUES ({vals});"


def build_vals(emit_defs: list[ColumnEmitDefinition]) -> str:
    formatters = _FORMATTERS
    parts: list[str] = []
    append = parts.append
    for ed in emit_defs:
        fmt = formatters.get(ed.data_type)
        append(str(ed.value) if fmt is None else fmt(ed.value))
    return ", ".join(parts)
