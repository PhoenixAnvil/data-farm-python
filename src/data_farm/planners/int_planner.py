from __future__ import annotations

from data_farm.emitters.sql import ColumnEmitDefinition
from data_farm.field.text import TextFieldDefinition
from data_farm.generators.text import TextGenerator
from data_farm.models.models import (
    ColumnInspection,  # adjust import
    PatternSuggestion,
)
from data_farm.patterns.base import Pattern
from data_farm.planners.context import PlanContext
from data_farm.utils.enums import SqlType


class IntPlanner:
    strategy = "int_range"

    def plan(
        self,
        column: ColumnInspection,
        suggestion: PatternSuggestion,
        ctx: PlanContext,
    ) -> ColumnEmitDefinition | None:
        pattern_key = self._pattern_key_for_strategy(suggestion.strategy)

        if pattern_key and ctx.patterns.exists(pattern_key):
            pattern = ctx.patterns.get(pattern_key)
        else:
            pattern = Pattern(classification="general_int", choices=["1", "3", "5", "7", "9"])

        field_def = TextFieldDefinition(
            allow_null=column.nullable,
            fixed_length=None,
            min_length=0,
            max_length=10,
        )

        value = TextGenerator(ctx.rng, pattern, field_def).generate()
        if value is None:
            return None

        return ColumnEmitDefinition(
            name=column.name,
            data_type=SqlType.STRING,
            value=value,
        )

    @staticmethod
    def _pattern_key_for_strategy(strategy: str) -> str | None:
        s = (strategy or "").strip().lower()
        if s == "age":
            return "ages"

        return None
