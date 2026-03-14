from __future__ import annotations

from data_farm.l0_domain.model.models import ColumnInspection
from data_farm.l0_domain.suggestors.defaults import build_default_registry
from data_farm.l0_domain.suggestors.engine import suggest_for_column


def test_suggest_for_column_never_returns_none(col_first_name: ColumnInspection) -> None:
    reg = build_default_registry()
    s = suggest_for_column(col_first_name, reg.all())
    assert s is not None


def test_suggest_for_column_is_deterministic_for_same_input(col_first_name: ColumnInspection) -> None:
    reg = build_default_registry()
    suggestors = reg.all()

    s1 = suggest_for_column(col_first_name, suggestors)
    s2 = suggest_for_column(col_first_name, suggestors)

    assert s1.strategy == s2.strategy
    assert s1.pattern_id == s2.pattern_id
    assert s1.suggestor == s2.suggestor
