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
