"""Emitter interfaces.

Emitters convert generated values into an output representation (e.g., SQL).
This module defines the Emitter contract shared across concrete emitters.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from data_farm.l0_domain.model.models import ColumnEmitDefinition


class Emitter(ABC):
    """TBD"""

    @abstractmethod
    def emit(self, table: str, emit_defs: list[ColumnEmitDefinition]) -> Iterable[str]:
        """TBD"""
        pass
