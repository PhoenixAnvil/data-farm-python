from __future__ import annotations

from data_farm.application.context import PlanContext
from data_farm.domain.enums import SqlType
from data_farm.domain.model.models import ColumnInspection, NormalizedColumnType, PatternSuggestion
from data_farm.domain.planners.numeric_planner import NumericPlanner


def test_numeric_planner_emits_value(plan_context: PlanContext) -> None:
    col = ColumnInspection(
        table="t1",
        name="amount",
        data_type=NormalizedColumnType(
            name=SqlType.DECIMAL,
            length=None,
            num_precision=10,
            scale=2,
            time_precision=None,
        ),
        nullable=False,
    )
    sug = PatternSuggestion(strategy="numeric", pattern_id=None, confidence=1.0, reason="t", suggestor="t", priority=0)
    ed = NumericPlanner().plan(col, sug, plan_context)
    assert ed is not None
    assert ed.data_type == SqlType.DECIMAL
    assert ed.value is not None
