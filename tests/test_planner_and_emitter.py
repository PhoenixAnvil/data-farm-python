from __future__ import annotations

from data_farm.application.context import PlanContext
from data_farm.domain.enums import SqlType
from data_farm.domain.model.models import ColumnEmitDefinition, ColumnInspection, PatternSuggestion
from data_farm.domain.planners.string_planner import StringPlanner
from data_farm.emitters.sql import SqlEmitter


def test_string_planner_uses_pattern_id_when_present(plan_context: PlanContext, col_first_name: ColumnInspection) -> None:
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
    for insert in e.emit(
        "t1",
        [
            ColumnEmitDefinition(name="first_name", data_type=SqlType.STRING, value="Alice"),
            ColumnEmitDefinition(name="age", data_type=SqlType.INTEGER, value="42"),
        ],
    ):
        assert insert == "INSERT INTO t1 (first_name, age) VALUES ('Alice', 42);"
