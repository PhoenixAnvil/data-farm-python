from __future__ import annotations

from data_farm.domain.enums import SqlType
from data_farm.domain.model.models import ColumnEmitDefinition
from data_farm.emitters.sql import SqlEmitter


def test_emitter_renders_null_without_quotes() -> None:
    e = SqlEmitter()
    cols = [ColumnEmitDefinition(name="note", data_type=SqlType.STRING, value=None)]
    sql = e.emit("t1", cols)
    sql_str = next(iter(sql))
    assert "NULL" in sql_str.upper()
    assert "'NULL'" not in sql_str.upper()


def test_emitter_renders_boolean_as_true_false() -> None:
    e = SqlEmitter()
    sql_true = e.emit("t1", [ColumnEmitDefinition("is_active", SqlType.BOOLEAN, True)])
    sql_false = e.emit("t1", [ColumnEmitDefinition("is_active", SqlType.BOOLEAN, False)])
    sql_true_str = next(iter(sql_true))
    sql_false_str = next(iter(sql_false))
    assert "TRUE" in sql_true_str.upper()
    assert "FALSE" in sql_false_str.upper()


def test_emitter_renders_numeric_without_quotes() -> None:
    e = SqlEmitter()
    sql = e.emit("t1", [ColumnEmitDefinition("amount", SqlType.DECIMAL, 12.34)])
    sql_str = next(iter(sql))
    # Conservative: ensure we didn't wrap numeric in single quotes
    assert "'12.34'" not in sql_str
    assert "12.34" in sql_str
