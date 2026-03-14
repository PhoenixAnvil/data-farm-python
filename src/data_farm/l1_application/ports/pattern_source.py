from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol


class PatternSource(Protocol):
    """Provides access to patterns (regardless of where they come from)."""

    def get_choices(self, pattern_name: str) -> Sequence[str]:
        """Return available pattern ids/names (no file extensions)."""
        ...
