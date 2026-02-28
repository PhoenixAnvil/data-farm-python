from __future__ import annotations

import random
from pathlib import Path

import pytest

from data_farm.models.models import ColumnInspection, NormalizedColumnType, PatternSuggestion
from data_farm.patterns.registry import PatternRegistry
from data_farm.planners.context import PlanContext
from data_farm.planners.string_planner import StringPlanner
from data_farm.utils.enums import SqlType


def test_string_planner_raises_when_pattern_file_empty(tmp_path: Path, rng_seeded: random.Random) -> None:
    d = tmp_path / "patterns"
    d.mkdir()
    (d / "empty.pat").write_text("# only comments\n\n", encoding="utf-8")
    reg = PatternRegistry(patterns_dir=d)
    ctx = PlanContext(rng=rng_seeded, patterns=reg, rows_per_table=3)

    col = ColumnInspection(
        table="t1",
        name="note",
        data_type=NormalizedColumnType(SqlType.STRING, 10, None, None, None),
        nullable=False,
        length=10,
    )
    sug = PatternSuggestion(strategy="string", pattern_id="empty", confidence=1.0, reason="t", suggestor="t", priority=0)
    with pytest.raises(ValueError) as excinfo:
        StringPlanner().plan(col, sug, ctx)

    assert "Pattern file is empty" in str(excinfo.value)


def test_string_planner_truncates_to_length(plan_context: PlanContext) -> None:
    TEST_LEN = 2
    col = ColumnInspection(
        table="t1",
        name="code",
        data_type=NormalizedColumnType(SqlType.STRING, 2, None, None, None),
        nullable=False,
        length=TEST_LEN,
    )
    sug = PatternSuggestion(
        strategy="string", pattern_id="first_names", confidence=1.0, reason="t", suggestor="t", priority=0
    )
    ed = StringPlanner().plan(col, sug, plan_context)
    assert ed is not None
    assert len(str(ed.value)) <= TEST_LEN
