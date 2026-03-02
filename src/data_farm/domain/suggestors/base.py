# data_farm/suggestors/base.py
from __future__ import annotations

from abc import ABC, abstractmethod

from data_farm.domain.model.models import ColumnInspection, PatternSuggestion


class PatternSuggestor(ABC):
    """
    Plugin interface. Keep it tiny.
    """

    # Unique stable identifier for logs/debug.
    name: str = "unnamed"

    # Higher priority wins ties on confidence.
    # Use this when multiple plugins match the same column.
    priority: int = 0

    @abstractmethod
    def suggest(self, col: ColumnInspection) -> PatternSuggestion | None:
        """
        Return a PatternSuggestion if this suggestor recognizes the column,
        otherwise return None.
        """
        raise NotImplementedError
