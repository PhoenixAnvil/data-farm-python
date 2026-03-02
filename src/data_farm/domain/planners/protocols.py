from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol

from data_farm.application.context import PlanContext
from data_farm.domain.enums import SqlType
from data_farm.domain.model.models import (
    ColumnEmitDefinition,
    ColumnInspection,  # adjust import
    PatternSuggestion,  # adjust import
)


class ColumnPlanner(Protocol):
    strategy: str  # registry key

    def plan(
        self,
        column: ColumnInspection,
        suggestion: PatternSuggestion,
        ctx: PlanContext,
    ) -> ColumnEmitDefinition | None: ...

    def compile(
        self,
        column: ColumnInspection,
        suggestion: PatternSuggestion,
        ctx: PlanContext,
    ) -> tuple[SqlType, Callable[[], Any | None]]: ...
