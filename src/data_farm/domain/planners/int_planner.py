from __future__ import annotations

from collections.abc import Callable
from typing import Any

from data_farm.application.context import PlanContext
from data_farm.domain.enums import SqlType
from data_farm.domain.generators.text import TextGenerator
from data_farm.domain.model.models import (
    ColumnInspection,  # adjust import
    PatternSuggestion,
)
from data_farm.emitters.sql import ColumnEmitDefinition
from data_farm.field.text import TextFieldDefinition


class IntPlanner:
    strategy = "int_range"

    def compile(
        self,
        column: ColumnInspection,
        suggestion: PatternSuggestion,
        ctx: PlanContext,
    ) -> tuple[SqlType, Callable[[], Any | None]]:
        """Compile a per-column generator to remove planning work from the hot row loop."""
        pattern_key = self._pattern_key_for_strategy(suggestion.strategy)

        if pattern_key and ctx.patterns.exists(pattern_key):
            choices = ctx.patterns.get_choices(pattern_key)
        else:
            choices = ["1", "3", "5", "7", "9"]

        field_def = TextFieldDefinition(
            allow_null=column.nullable,
            fixed_length=None,
            min_length=0,
            max_length=10,
        )

        gen = TextGenerator(ctx.rng, choices, field_def)
        return (SqlType.STRING, gen.generate)

    def plan(
        self,
        column: ColumnInspection,
        suggestion: PatternSuggestion,
        ctx: PlanContext,
    ) -> ColumnEmitDefinition | None:
        pattern_key = self._pattern_key_for_strategy(suggestion.strategy)

        if pattern_key and ctx.patterns.exists(pattern_key):
            choices = ctx.patterns.get_choices(pattern_key)
        else:
            choices = ["1", "3", "5", "7", "9"]

        field_def = TextFieldDefinition(
            allow_null=column.nullable,
            fixed_length=None,
            min_length=0,
            max_length=10,
        )

        value = TextGenerator(ctx.rng, choices, field_def).generate()
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
