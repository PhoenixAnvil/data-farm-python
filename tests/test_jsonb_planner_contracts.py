from __future__ import annotations

from data_farm.l0_domain.enums import SqlType
from data_farm.l0_domain.model.models import ColumnInspection, NormalizedColumnType, PatternSuggestion
from data_farm.l0_domain.planners.jsonb_planner import JSONBPlanner
from data_farm.l1_application.plan.context import PlanContext


def test_jsonb_planner_emits_json_string(plan_context: PlanContext) -> None:
    col = ColumnInspection(
        table="t1",
        name="payload",
        data_type=NormalizedColumnType(
            name=SqlType.JSONB,
            length=None,
            num_precision=None,
            scale=None,
            time_precision=None,
        ),
        nullable=False,
    )
    sug = PatternSuggestion(strategy="jsonb", pattern_id=None, confidence=1.0, reason="t", suggestor="t", priority=0)
    ed = JSONBPlanner().plan(col, sug, plan_context)
    assert ed is not None
    assert ed.data_type == SqlType.JSONB
    assert isinstance(ed.value, str)
    assert ed.value.strip().startswith("{")
