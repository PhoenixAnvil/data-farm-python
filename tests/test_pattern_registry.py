from __future__ import annotations

from pathlib import Path

from data_farm.infrastructure.patterns.filesystem_pattern_source import FilesystemPatternSource


def test_pattern_registry_get_choices_loads_and_normalizes(patterns_dir: Path) -> None:
    reg = FilesystemPatternSource(patterns_dir=patterns_dir)

    choices = reg.get_choices("First Names")  # exercises normalization -> first_names.pat
    assert choices == ["Alice", "Bob", "Charlie"]


def test_pattern_registry_caches_loaded_patterns(patterns_dir: Path) -> None:
    reg = FilesystemPatternSource(patterns_dir=patterns_dir)

    p1 = reg.get_choices("first_names")
    p2 = reg.get_choices("first_names")
    assert p1 is p2  # cached instance
