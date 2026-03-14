from __future__ import annotations

from dataclasses import dataclass

from data_farm.l0_domain.model.models import PatternSuggestion
from data_farm.l0_domain.planners.protocols import ColumnPlanner


@dataclass(frozen=True)
class GenerationPlan:
    table: str
    column: str
    suggestion: PatternSuggestion
    col_planner: ColumnPlanner
