from __future__ import annotations

from data_farm.l0_domain.enums import SqlType
from data_farm.l0_domain.model.models import ColumnInspection, PatternSuggestion
from data_farm.l0_domain.planners.string_planner import StringPlanner
from data_farm.l1_application.plan.context import PlanContext


def test_string_planner_falls_back_when_pattern_missing(
    plan_context: PlanContext, col_short_string: ColumnInspection
) -> None:
    planner = StringPlanner()
    # request a missing pattern id; planner should still return an emit definition (fallback)
    suggestion = PatternSuggestion(
        strategy="string",
        pattern_id="missing_pattern",
        confidence=0.9,
        reason="test",
        suggestor="test",
        priority=0,
    )

    ed = planner.plan(col_short_string, suggestion, plan_context)
    assert ed is not None
    assert ed.data_type == SqlType.STRING
    assert ed.value is not None


def test_string_planner_respects_column_length(col_short_string: ColumnInspection, plan_context: PlanContext) -> None:
    COL_LEN = 8
    planner = StringPlanner()
    suggestion = PatternSuggestion(
        strategy="string",
        pattern_id="first_names",  # values include longer names, but col length is 8
        confidence=0.9,
        reason="test",
        suggestor="test",
        priority=0,
    )
    ed = planner.plan(col_short_string, suggestion, plan_context)
    assert ed is not None
    assert isinstance(ed.value, str)
    assert len(ed.value) <= COL_LEN
