from __future__ import annotations

from data_farm.domain.enums import SqlType
from data_farm.domain.model.models import ColumnEmitDefinition
from data_farm.emitters.sql import SqlEmitter


def test_sql_emitter_renders_insert_statement() -> None:
    e = SqlEmitter()
    cols = [
        ColumnEmitDefinition(name="first_name", data_type=SqlType.STRING, value="Alice"),
        ColumnEmitDefinition(name="code", data_type=SqlType.STRING, value="X1"),
    ]
    sql = e.emit("t1", cols)
    sql_str = next(iter(sql))
    assert "INSERT" in sql_str.upper()
    assert "t1" in sql_str
    assert "first_name" in sql_str
    assert "Alice" in sql_str


def test_sql_emitter_escapes_single_quotes() -> None:
    e = SqlEmitter()
    cols = [ColumnEmitDefinition(name="note", data_type=SqlType.STRING, value="Bob's bike")]
    sql = e.emit("t1", cols)
    sql_str = next(iter(sql))
    # standard SQL escape is doubling quotes
    assert "Bob''s bike" in sql_str
