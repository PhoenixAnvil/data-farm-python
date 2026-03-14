from __future__ import annotations

from pathlib import Path
from typing import Protocol


class PatternSource(Protocol):
    """Domain port for looking up pattern choices by id."""

    def get_choices(self, pattern_name: str) -> list[str]:
        """Return the choices for the pattern id, or an empty list if missing."""
        ...

    def exists(self, pattern_name: str) -> bool: ...

    def _load_pattern_file(self, key: str) -> list[str]: ...

    def _pattern_path(self, key: str) -> Path: ...

    @staticmethod
    def _norm_key(name: str) -> str: ...
