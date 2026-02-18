from __future__ import annotations

from dataclasses import dataclass

from data_farm.models.models import PatternSuggestion
from data_farm.planners.protocols import ColumnPlanner


@dataclass(frozen=True)
class GenerationPlan:
    table: str
    column: str
    suggestion: PatternSuggestion
    col_planner: ColumnPlanner
