from __future__ import annotations

from data_farm.models.models import PatternSuggestion
from data_farm.suggestors.engine import choose_best


def test_choose_best_prefers_higher_confidence() -> None:
    a = PatternSuggestion(strategy="a", pattern_id=None, confidence=0.6, reason="a", suggestor="a", priority=0)
    b = PatternSuggestion(strategy="b", pattern_id=None, confidence=0.9, reason="b", suggestor="b", priority=0)
    best = choose_best([a, b])
    assert best is b


def test_choose_best_ties_break_by_priority() -> None:
    a = PatternSuggestion(strategy="a", pattern_id=None, confidence=0.9, reason="a", suggestor="a", priority=10)
    b = PatternSuggestion(strategy="b", pattern_id=None, confidence=0.9, reason="b", suggestor="b", priority=99)
    best = choose_best([a, b])
    assert best is b
