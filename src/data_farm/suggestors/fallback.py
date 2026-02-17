from __future__ import annotations

from data_farm.models.models import ColumnInspection, PatternSuggestion
from data_farm.utils.enums import SqlType


def type_based_fallback(col: ColumnInspection) -> PatternSuggestion:
    t = col.data_type.name
    n = col.name.lower()

    strategy, reason = _fallback_strategy(t, n, col.length)

    return PatternSuggestion(
        strategy=strategy,
        confidence=0.10,
        reason=reason,
        suggestor="type_fallback",
        priority=-1,
    )


def _fallback_strategy(sql_type: SqlType, col_name: str, length: int | None) -> tuple[str, str]:
    # Exact / high-signal type
    if sql_type == SqlType.UUID:
        return "uuid", "fallback: UUID type"

    elif sql_type == SqlType.BOOLEAN:
        return "bool", "fallback: boolean type"

    elif sql_type == SqlType.INTEGER:
        return _int_fallback(col_name)

    elif sql_type == SqlType.DECIMAL:
        return "decimal_amount", "fallback: numeric type"

    elif sql_type == SqlType.DATE:
        return "date_recent", "fallback: date type"

    elif sql_type == SqlType.DATETIME:
        return "datetime_recent", "fallback: datetime/timestamp type"

    elif sql_type == SqlType.STRING:
        return _string_fallback(length)

    return "string", "fallback: unknown type treated as string"


def _int_fallback(n: str) -> tuple[str, str]:
    if "age" in n:
        return "int_age", "fallback: integer type + name suggests age"

    if any(k in n for k in ("count", "qty", "quantity", "num", "number")):
        return "int_count", "fallback: integer type + name suggests count"

    return "int_range", "fallback: integer type"


def _string_fallback(length: int | None) -> tuple[str, str]:
    max_short_str_len = 16
    if length is not None and length <= max_short_str_len:
        return "string_short", "fallback: short string column"
    return "string", "fallback: string column"
