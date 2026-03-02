# data_farm/suggestors/registry.py
from __future__ import annotations

from collections.abc import Iterable

from data_farm.domain.suggestors.base import PatternSuggestor


class SuggestorRegistry:
    """
    Simple in-repo registry. Later you can swap this for entry points
    without changing the engine logic.
    """

    def __init__(self) -> None:
        self._items: list[PatternSuggestor] = []

    def register(self, suggestor: PatternSuggestor) -> None:
        self._items.append(suggestor)

    def register_many(self, suggestors: Iterable[PatternSuggestor]) -> None:
        self._items.extend(suggestors)

    def all(self) -> list[PatternSuggestor]:
        # You can sort here if you want consistent ordering.
        return list(self._items)
