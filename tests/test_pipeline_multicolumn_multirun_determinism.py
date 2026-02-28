from __future__ import annotations

import random
from pathlib import Path

from data_farm.emitters.sql import SqlEmitter
from data_farm.models.models import ColumnInspection, NormalizedColumnType, PatternSuggestion
from data_farm.patterns.registry import PatternRegistry
from data_farm.planners.context import PlanContext
from data_farm.planners.registry import PlannerRegistry
from data_farm.utils.enums import SqlType


# ruff: noqa: PLR0915
def test_two_column_row_generation_is_repeatable(tmp_path: Path) -> None:
    # Build patterns
    d = tmp_path / "patterns"
    d.mkdir()
    (d / "first_names.pat").write_text("Alice\nBob\nCharlie\n", encoding="utf-8")
    (d / "email.pat").write_text("a@example.com\nb@example.com\n", encoding="utf-8")
    reg = PatternRegistry(patterns_dir=d)

    ctx1 = PlanContext(rng=random.Random(123), patterns=reg, rows_per_table=3)
    ctx2 = PlanContext(rng=random.Random(123), patterns=reg, rows_per_table=3)

    # Columns and suggestions
    col1 = ColumnInspection(
        table="t1",
        name="first_name",
        data_type=NormalizedColumnType(SqlType.STRING, 100, None, None, None),
        nullable=False,
        length=32,
    )  # type ignored by StringPlanner
    col2 = ColumnInspection(
        table="t1",
        name="email",
        data_type=NormalizedColumnType(SqlType.STRING, 100, None, None, None),
        nullable=False,
        length=64,
    )

    s1 = PatternSuggestion(
        strategy="string", pattern_id="first_names", confidence=1.0, reason="t", suggestor="t", priority=0
    )
    s2 = PatternSuggestion(strategy="email", pattern_id="email", confidence=1.0, reason="t", suggestor="t", priority=0)

    preg = PlannerRegistry.default()
    p_string = preg.get("string")
    assert p_string is not None
    p_email = preg.get("email")
    assert p_email is not None

    eds1 = [p_string.plan(col1, s1, ctx1), p_email.plan(col2, s2, ctx1)]
    assert eds1[0] is not None
    assert eds1[1] is not None

    eds2 = [p_string.plan(col1, s1, ctx2), p_email.plan(col2, s2, ctx2)]
    assert eds2[0] is not None
    assert eds2[1] is not None

    e = SqlEmitter()
    sql1 = next(iter(e.emit("t1", [eds1[0], eds1[1]])))
    sql2 = next(iter(e.emit("t1", [eds2[0], eds2[1]])))

    assert sql1 == sql2
