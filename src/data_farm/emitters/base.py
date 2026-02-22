"""
Defines the contract that all Emitters implement.

This module has one primary role--define the contract
that all Emitters must implement.

An Emitter accepts a table name and a list of
``ColumnEmitDefinitions``.

An Emitter returns an Iterable containing str objects.

This module does not:
- Inspect column metadata
--Generate value sets
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from data_farm.models.models import ColumnEmitDefinition


class Emitter(ABC):
    """TBD"""

    @abstractmethod
    def emit(self, table: str, emit_defs: list[ColumnEmitDefinition]) -> Iterable[str]:
        """TBD"""
        pass
