from __future__ import annotations

from pathlib import Path

import pytest

from data_farm.infrastructure.patterns.filesystem_pattern_source import FilesystemPatternSource


def test_pattern_registry_ignores_blank_and_comment_lines(tmp_path: Path) -> None:
    d = tmp_path / "patterns"
    d.mkdir()
    (d / "codes.pat").write_text("# header\n\nA\n\n# mid\nB\n", encoding="utf-8")

    reg = FilesystemPatternSource(patterns_dir=d)
    choices = reg.get_choices("codes")

    assert choices is not None
    assert choices == ["A", "B"]


def test_pattern_registry_missing_pattern_raises_file_not_found(tmp_path: Path) -> None:
    d = tmp_path / "patterns" / "nope.pat"
    pattern = FilesystemPatternSource(patterns_dir=d)
    with pytest.raises(FileNotFoundError) as excinfo:
        pattern.get_choices("does_not_exist")

    assert "Pattern file not found" in str(excinfo.value)


def test_pattern_registry_caches_instances(tmp_path: Path) -> None:
    d = tmp_path / "patterns"
    d.mkdir(parents=True, exist_ok=True)
    p = d / "first_names.pat"
    p.write_text("Alice\nBob\n", encoding="utf-8")
    src = FilesystemPatternSource(patterns_dir=d)
    a = src.get_choices(pattern_name="first_names")
    b = src.get_choices(pattern_name="first_names")
    assert a is b  # cache hit should return same object
