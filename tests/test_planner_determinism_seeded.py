from __future__ import annotations

import random

from data_farm.models.models import ColumnInspection, PatternSuggestion
from data_farm.patterns.registry import PatternRegistry
from data_farm.planners.context import PlanContext
from data_farm.planners.string_planner import StringPlanner


def test_string_planner_is_repeatable_given_seed(
    col_first_name: ColumnInspection, pattern_registry: PatternRegistry
) -> None:
    suggestion = PatternSuggestion(
        strategy="string", pattern_id="first_names", confidence=1.0, reason="t", suggestor="t", priority=0
    )

    ctx1 = PlanContext(rng=random.Random(123), patterns=pattern_registry, rows_per_table=3)
    ctx2 = PlanContext(rng=random.Random(123), patterns=pattern_registry, rows_per_table=3)

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
