from __future__ import annotations

from pathlib import Path

import pytest

from data_farm.patterns.registry import PatternRegistry


def test_pattern_registry_invalid_dir_raises(tmp_path: Path) -> None:
    bad = tmp_path / "nope"
    with pytest.raises(FileNotFoundError) as excinfo:
        PatternRegistry(patterns_dir=bad).get("test")

    assert "Pattern file not found" in str(excinfo.value)
