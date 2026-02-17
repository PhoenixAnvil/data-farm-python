from __future__ import annotations

from data_farm.emitters.sql import SqlEmitter
from data_farm.models.models import ColumnEmitDefinition, PatternSuggestion
from data_farm.planners.string_planner import StringPlanner
from data_farm.utils.enums import SqlType


def test_string_planner_uses_pattern_id_when_present(plan_context, col_first_name) -> None:
    planner = StringPlanner()

    suggestion = PatternSuggestion(
        strategy="string",
        pattern_id="first_names",
        confidence=1.0,
        reason="test",
        suggestor="unit_test",
        priority=0,
    )

    ed = planner.plan(col_first_name, suggestion, plan_context)
    assert ed is not None
    assert ed.value in {"Alice", "Bob", "Charlie"}
    assert ed.data_type == SqlType.STRING


def test_sql_emitter_quotes_string_values() -> None:
    e = SqlEmitter()
    sql = e.emit(
        "t1",
        [
            ColumnEmitDefinition(name="first_name", data_type=SqlType.STRING, value="Alice"),
            ColumnEmitDefinition(name="age", data_type=SqlType.INTEGER, value="42"),
        ],
    )
    assert sql == "INSERT INTO t1 (first_name, age) VALUES ('Alice', 42);"
