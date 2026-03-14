from __future__ import annotations

from pathlib import Path

from data_farm.l2_interface_adapters.patterns.filesystem_pattern_source import FilesystemPatternSource


def test_pattern_registry_strips_bom_and_whitespace(tmp_path: Path) -> None:
    d = tmp_path / "patterns"
    d.mkdir()
    # UTF-8 BOM + spaces + CRLF
    raw = "\ufeff  Alpha  \r\n  Beta\r\n# comment\r\n\r\n  Gamma  \r\n"
    (d / "vals.pat").write_text(raw, encoding="utf-8")

    reg = FilesystemPatternSource(patterns_dir=d)
    choices = reg.get_choices("vals")
    assert choices is not None
    assert choices == ["Alpha", "Beta", "Gamma"]
