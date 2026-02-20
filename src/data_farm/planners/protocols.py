from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol

from data_farm.models.models import (
    ColumnEmitDefinition,
    ColumnInspection,  # adjust import
    PatternSuggestion,  # adjust import
)
from data_farm.planners.context import PlanContext
from data_farm.utils.enums import SqlType


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
