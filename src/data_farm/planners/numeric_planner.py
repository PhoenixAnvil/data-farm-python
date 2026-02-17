from __future__ import annotations

import random
from decimal import Decimal

from data_farm.emitters.sql import ColumnEmitDefinition
from data_farm.field.text import TextFieldDefinition
from data_farm.generators.text import TextGenerator
from data_farm.messages.messages import msg
from data_farm.models.models import (
    ColumnInspection,  # adjust import
    PatternSuggestion,
)
from data_farm.patterns.base import Pattern
from data_farm.planners.context import PlanContext
from data_farm.utils.enums import SqlType


class NumericPlanner:
    strategy = "decimal_amount"

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
            pattern = Pattern(classification="general_decimal", choices=[str(self.generate_numeric(random.Random(), 8, 3))])

        field_def = TextFieldDefinition(
            allow_null=column.nullable,
            fixed_length=None,
            min_length=0,
            max_length=100,
        )

        value = TextGenerator(ctx.rng, pattern, field_def).generate()
        if value is None:
            return None

        return ColumnEmitDefinition(
            name=column.name,
            data_type=SqlType.DECIMAL,
            value=value,
        )

    @staticmethod
    def _pattern_key_for_strategy(strategy: str) -> str | None:
        s = (strategy or "").strip().lower()
        if s == "age":
            return "ages"

        return None

    def generate_numeric(self, rng: random.Random, precision: int, scale: int) -> Decimal:
        if precision <= 0:
            raise ValueError(msg("err.planner.numeric.precision"))
        if scale < 0 or scale > precision:
            raise ValueError(msg("error.planner.numeric.scale"))

        max_abs_int = (10**precision) - 1
        n = rng.randint(-max_abs_int, max_abs_int)

        divisor = Decimal(10) ** scale
        return Decimal(n) / divisor
