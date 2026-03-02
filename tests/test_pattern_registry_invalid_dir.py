from __future__ import annotations

from pathlib import Path

import pytest

from data_farm.infrastructure.patterns.filesystem_pattern_source import FilesystemPatternSource


def test_pattern_registry_invalid_dir_raises(tmp_path: Path) -> None:
    bad = tmp_path / "nope"
    with pytest.raises(FileNotFoundError) as excinfo:
        FilesystemPatternSource(patterns_dir=bad).get_choices("test")

    assert "Pattern file not found" in str(excinfo.value)
