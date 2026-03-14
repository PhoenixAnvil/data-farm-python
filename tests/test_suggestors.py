from __future__ import annotations

from data_farm.l0_domain.model.models import ColumnInspection, PatternSuggestion
from data_farm.l0_domain.suggestors.defaults import build_default_registry
from data_farm.l0_domain.suggestors.engine import suggest_for_column


def test_suggest_for_column_selects_first_name(col_first_name: ColumnInspection) -> None:
    reg = build_default_registry()
    suggestors = reg.all()

    suggestion = suggest_for_column(col_first_name, suggestors)

    CONFIDENCE = 0.9

    assert suggestion.strategy == "string"  # planner strategy stays generic
    assert suggestion.pattern_id == "first_names"
    assert suggestion.suggestor == "first_name"
    assert suggestion.confidence >= CONFIDENCE


def test_suggest_for_column_falls_back_when_no_suggestors(col_short_string: ColumnInspection) -> None:
    suggestion = suggest_for_column(col_short_string, [])
    assert isinstance(suggestion, PatternSuggestion)
    assert suggestion.suggestor == "type_fallback"
    # For short strings, fallback strategy is 'string_short'
    assert suggestion.strategy == "string_short"
