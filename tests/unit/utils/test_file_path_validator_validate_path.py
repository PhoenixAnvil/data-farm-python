from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

from data_farm.messages.messages import msg
from data_farm.utils.path import FilePathValidator


# Happy Path
def test_validate_path_returns_path_for_existing_file(tmp_path: Path) -> None:
    p = tmp_path / "file.txt"
    p.write_text("ok")

    result = FilePathValidator(str(p)).validate_path()

    assert result == p


# Type alias for our scenario builder
MakePath = Callable[[Path], Path | None]


# --- Scenario builders (no lambdas) ---


def make_none(_: Path) -> None:
    return None


def make_missing(tmp: Path) -> Path:
    return tmp / "missing.txt"


def make_directory(tmp: Path) -> Path:
    return tmp


# --- Parametrized test ---


@pytest.mark.parametrize(
    ("make_path", "exc_type", "expected_key"),
    [
        (make_none, ValueError, "err.utils.path.no_src"),
        (make_missing, FileNotFoundError, "err.utils.path.no_exist"),
        (make_directory, ValueError, "err.utils.path.not_file"),
    ],
)
def test_validate_path_error_cases(
    tmp_path: Path,
    make_path: MakePath,
    exc_type: type[Exception],
    expected_key: str,
) -> None:
    # Arrange
    p = make_path(tmp_path)
    validator = FilePathValidator(str(p) if p is not None else None)

    # Act
    with pytest.raises(exc_type) as excinfo:
        validator.validate_path()

    # Assert
    expected = msg(expected_key) if p is None else msg(expected_key, path=p)
    assert expected in str(excinfo.value)
