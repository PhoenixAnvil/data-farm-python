from __future__ import annotations

from typing import Protocol

from data_farm.emitters.sql import ColumnEmitDefinition
from data_farm.models.models import (
    ColumnInspection,  # adjust import
    PatternSuggestion,  # adjust import
)
from data_farm.planners.context import PlanContext


class ColumnPlanner(Protocol):
    strategy: str  # registry key

    def plan(
        self,
        column: ColumnInspection,
        suggestion: PatternSuggestion,
        ctx: PlanContext,
    ) -> ColumnEmitDefinition | None: ...
