from __future__ import annotations

from pathlib import Path

from data_farm.patterns.registry import PatternRegistry


def test_pattern_registry_strips_bom_and_whitespace(tmp_path: Path) -> None:
    d = tmp_path / "patterns"
    d.mkdir()
    # UTF-8 BOM + spaces + CRLF
    raw = "\ufeff  Alpha  \r\n  Beta\r\n# comment\r\n\r\n  Gamma  \r\n"
    (d / "vals.pat").write_text(raw, encoding="utf-8")

    reg = PatternRegistry(patterns_dir=d)
    pat = reg.get("vals")
    assert pat is not None
    assert pat.choices == ["Alpha", "Beta", "Gamma"]
