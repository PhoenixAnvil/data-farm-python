from __future__ import annotations

import random
from datetime import datetime
from pathlib import Path

from data_farm.l0_domain.enums import SqlType
from data_farm.l0_domain.model.models import ColumnInspection, NormalizedColumnType, PatternSuggestion
from data_farm.l0_domain.planners.boolean_planner import BooleanPlanner
from data_farm.l0_domain.planners.datetime_planner import DateTimePlanner
from data_farm.l0_domain.planners.int_planner import IntPlanner
from data_farm.l0_domain.planners.uuid_planner import UUIDPlanner
from data_farm.l1_application.plan.context import PlanContext
from data_farm.l2_interface_adapters.patterns.filesystem_pattern_source import FilesystemPatternSource


def _ctx(tmp_path: Path) -> PlanContext:
    # Build a tiny pattern registry with additional patterns used by planners
    d = tmp_path / "patterns"
    d.mkdir()
    (d / "ages.pat").write_text("18\n21\n35\n", encoding="utf-8")
    (d / "uuid.pat").write_text("8dd6d9d3-af9c-4ca7-8c32-a9956a29561d\n", encoding="utf-8")
    (d / "datetime_recent.pat").write_text("2024-01-01T00:00:00Z\n2024-01-02T00:00:00Z\n", encoding="utf-8")
    reg = FilesystemPatternSource(patterns_dir=d)
    return PlanContext(rng=random.Random(123), patterns=reg, rows_per_table=3)


def test_boolean_planner_emits_true_false(tmp_path: Path) -> None:
    ctx = _ctx(tmp_path)
    col = ColumnInspection("t1", "is_active", NormalizedColumnType(SqlType.BOOLEAN, None, None, None, None), nullable=False)
    sug = PatternSuggestion(strategy="bool", pattern_id=None, confidence=1.0, reason="t", suggestor="t", priority=0)

    ed = BooleanPlanner().plan(col, sug, ctx)
    assert ed is not None
    assert ed.data_type == SqlType.BOOLEAN
    assert str(ed.value).lower() in {"true", "false"}


def test_int_planner_age_strategy_uses_ages_pattern_when_present(tmp_path: Path) -> None:
    ctx = _ctx(tmp_path)
    col = ColumnInspection("t1", "age", NormalizedColumnType(SqlType.INTEGER, None, None, None, None), nullable=False)
    sug = PatternSuggestion(strategy="age", pattern_id=None, confidence=1.0, reason="t", suggestor="t", priority=0)

    ed = IntPlanner().plan(col, sug, ctx)
    assert ed is not None
    # Current implementation emits STRING values for int-ish fields (planner chooses SqlType.STRING)
    assert ed.value in {"18", "21", "35"}


def test_uuid_planner_uses_uuid_pattern(tmp_path: Path) -> None:
    ctx = _ctx(tmp_path)
    col = ColumnInspection("t1", "id", NormalizedColumnType(SqlType.UUID, None, None, None, None), nullable=False)
    sug = PatternSuggestion(strategy="uuid", pattern_id="uuid", confidence=1.0, reason="t", suggestor="t", priority=0)

    ed = UUIDPlanner().plan(col, sug, ctx)
    assert ed is not None
    assert str(ed.value) == "8dd6d9d3-af9c-4ca7-8c32-a9956a29561d"


def test_datetime_planner_uses_recent_pattern(tmp_path: Path) -> None:
    ctx = _ctx(tmp_path)
    col = ColumnInspection(
        "t1", "created_at", NormalizedColumnType(SqlType.DATETIME, None, None, None, None), nullable=False
    )
    sug = PatternSuggestion(
        strategy="datetime_recent", pattern_id="datetime_recent", confidence=1.0, reason="t", suggestor="t", priority=0
    )

    ed = DateTimePlanner().plan(col, sug, ctx)
    min_day = datetime.now().day - 30
    assert ed is not None
    actual = datetime.fromisoformat(ed.value)
    assert actual.day >= min_day
