from __future__ import annotations

from collections.abc import Callable
from typing import Any

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


class UUIDPlanner:
    strategy = "uuid"

    def compile(
        self,
        column: ColumnInspection,
        suggestion: PatternSuggestion,
        ctx: PlanContext,
    ) -> tuple[SqlType, Callable[[], Any | None]]:
        """Compile a per-column generator to remove planning work from the hot row loop."""
        pattern_key = self._pattern_key_for_strategy(suggestion.strategy)

        if pattern_key and ctx.patterns.exists(pattern_key):
            pattern = ctx.patterns.get(pattern_key)
        else:
            pattern = Pattern(
                classification="general_uuid",
                choices=["8dd6d9d3-af9c-4ca7-8c32-a9956a29561d", "2e054344-0ae3-4093-831d-2423f2f01ca2"],
            )

        field_def = TextFieldDefinition(
            allow_null=column.nullable,
            fixed_length=None,
            min_length=0,
            max_length=200,
        )

        gen = TextGenerator(ctx.rng, pattern, field_def)
        return (SqlType.UUID, gen.generate)

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
            pattern = Pattern(
                classification="general_uuid",
                choices=["8dd6d9d3-af9c-4ca7-8c32-a9956a29561d", "2e054344-0ae3-4093-831d-2423f2f01ca2"],
            )

        field_def = TextFieldDefinition(
            allow_null=column.nullable,
            fixed_length=None,
            min_length=0,
            max_length=200,
        )

        value = TextGenerator(ctx.rng, pattern, field_def).generate()
        if value is None:
            return None

        return ColumnEmitDefinition(
            name=column.name,
            data_type=SqlType.UUID,
            value=value,
        )

    @staticmethod
    def _pattern_key_for_strategy(strategy: str) -> str | None:
        s = (strategy or "").strip().lower()
        if s == "age":
            return "ages"

        return None
