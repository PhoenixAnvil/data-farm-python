from __future__ import annotations

from data_farm.application.context import PlanContext
from data_farm.domain.model.models import ColumnInspection, PatternSuggestion
from data_farm.domain.planners.boolean_planner import BooleanPlanner
from data_farm.domain.planners.datetime_planner import DateTimePlanner
from data_farm.domain.planners.int_planner import IntPlanner
from data_farm.domain.planners.uuid_planner import UUIDPlanner


def test_boolean_planner_compile_returns_callable(plan_context: PlanContext, col_short_string: ColumnInspection) -> None:
    sug = PatternSuggestion(strategy="bool", pattern_id=None, confidence=1.0, reason="t", suggestor="t", priority=0)
    sql_type, gen = BooleanPlanner().compile(col_short_string, sug, plan_context)
    v = gen()
    assert v in {"true", "false"}
    assert sql_type is not None


def test_int_planner_compile_returns_callable(plan_context: PlanContext, col_short_string: ColumnInspection) -> None:
    sug = PatternSuggestion(strategy="int_range", pattern_id=None, confidence=1.0, reason="t", suggestor="t", priority=0)
    sql_type, gen = IntPlanner().compile(col_short_string, sug, plan_context)
    v = gen()
    assert v is not None
    assert str(v).isdigit()
    assert sql_type is not None


def test_uuid_planner_compile_returns_uuid_like_string(
    plan_context: PlanContext, col_short_string: ColumnInspection
) -> None:
    sug = PatternSuggestion(strategy="uuid", pattern_id="uuid", confidence=1.0, reason="t", suggestor="t", priority=0)
    sql_type, gen = UUIDPlanner().compile(col_short_string, sug, plan_context)
    v = gen()
    assert v is not None
    assert "-" in str(v)
    assert sql_type is not None


def test_datetime_planner_compile_returns_iso_like_string(
    plan_context: PlanContext, col_short_string: ColumnInspection
) -> None:
    sug = PatternSuggestion(
        strategy="datetime_recent", pattern_id="datetime_recent", confidence=1.0, reason="t", suggestor="t", priority=0
    )
    sql_type, gen = DateTimePlanner().compile(col_short_string, sug, plan_context)
    v = gen()
    assert v is not None
    assert "T" in str(v) or "-" in str(v)
    assert sql_type is not None
