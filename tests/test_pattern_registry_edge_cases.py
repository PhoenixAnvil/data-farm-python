from __future__ import annotations

from pathlib import Path

import pytest

from data_farm.patterns.registry import PatternRegistry


def test_pattern_registry_ignores_blank_and_comment_lines(tmp_path: Path) -> None:
    d = tmp_path / "patterns"
    d.mkdir()
    (d / "codes.pat").write_text("# header\n\nA\n\n# mid\nB\n", encoding="utf-8")

    reg = PatternRegistry(patterns_dir=d)
    pat = reg.get("codes")

    assert pat is not None
    assert pat.choices == ["A", "B"]


def test_pattern_registry_missing_pattern_raises_file_not_found(pattern_registry: PatternRegistry) -> None:
    with pytest.raises(FileNotFoundError) as excinfo:
        pattern_registry.get("does_not_exist")

    assert "Pattern file not found" in str(excinfo.value)


def test_pattern_registry_caches_instances(pattern_registry: PatternRegistry) -> None:
    a = pattern_registry.get("first_names")
    b = pattern_registry.get("first_names")
    assert a is b  # cache hit should return same object
