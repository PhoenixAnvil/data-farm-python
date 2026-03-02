# data_farm/suggestors/engine.py
from __future__ import annotations

from collections.abc import Iterable

from data_farm.domain.model.models import ColumnInspection, PatternSuggestion
from data_farm.domain.suggestors.base import PatternSuggestor
from data_farm.domain.suggestors.fallback import type_based_fallback


def choose_best(
    suggestions: list[PatternSuggestion],
) -> PatternSuggestion | None:
    if not suggestions:
        return None

    # Sort by: confidence desc, priority desc, then stable (original order preserved by sort stability if equal)
    suggestions.sort(key=lambda s: (s.confidence, s.priority), reverse=True)
    return suggestions[0]


def suggest_for_column(
    col: ColumnInspection,
    suggestors: Iterable[PatternSuggestor],
) -> PatternSuggestion:
    """
    Run all suggestors; if none match, return type-based fallback.
    """
    suggestions: list[PatternSuggestion] = []

    for s in suggestors:
        suggestion = s.suggest(col)
        if suggestion is not None:
            suggestions.append(suggestion)

    best = choose_best(suggestions)
    if best is not None:
        return best

    return type_based_fallback(col)
