from __future__ import annotations

from pathlib import Path

import pytest

from data_farm.patterns.registry import PatternRegistry


def test_pattern_registry_get_loads_and_normalizes(patterns_dir: Path) -> None:
    reg = PatternRegistry(patterns_dir=patterns_dir)

    pat = reg.get("First Names")  # exercises normalization -> first_names.pat
    assert pat.classification == "first_names"
    assert pat.choices == ["Alice", "Bob", "Charlie"]


def test_pattern_registry_caches_loaded_patterns(patterns_dir: Path) -> None:
    reg = PatternRegistry(patterns_dir=patterns_dir)

    p1 = reg.get("first_names")
    p2 = reg.get("first_names")
    assert p1 is p2  # cached instance
