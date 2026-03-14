from __future__ import annotations

import random

from data_farm.l0_domain.model.models import ColumnInspection, PatternSuggestion
from data_farm.l0_domain.planners.string_planner import StringPlanner
from data_farm.l0_domain.ports.pattern_source import PatternSource
from data_farm.l1_application.plan.context import PlanContext


def test_string_planner_is_repeatable_given_seed(col_first_name: ColumnInspection, pattern_source: PatternSource) -> None:
    suggestion = PatternSuggestion(
        strategy="string", pattern_id="first_names", confidence=1.0, reason="t", suggestor="t", priority=0
    )

    ctx1 = PlanContext(rng=random.Random(123), patterns=pattern_source, rows_per_table=3)
    ctx2 = PlanContext(rng=random.Random(123), patterns=pattern_source, rows_per_table=3)

    p = StringPlanner()

    v1: list[str] = []
    for _ in range(5):
        ed = p.plan(col_first_name, suggestion, ctx1)
        assert ed is not None
        v1.append(ed.value)

    v2: list[str] = []
    for _ in range(5):
        ed = p.plan(col_first_name, suggestion, ctx2)
        assert ed is not None
        v2.append(ed.value)

    assert v1 == v2
