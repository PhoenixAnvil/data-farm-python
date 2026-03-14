# src/data_farm/planners/string_planner.py
from __future__ import annotations

from collections.abc import Callable
from typing import Any

from data_farm.field.text import TextFieldDefinition
from data_farm.l0_domain.enums import SqlType
from data_farm.l0_domain.generators.text import TextGenerator
from data_farm.l0_domain.model.models import ColumnEmitDefinition, ColumnInspection, PatternSuggestion
from data_farm.l1_application.plan.context import PlanContext


class StringPlanner:
    # Handles both fallback strategies
    strategy = "string"

    def compile(
        self,
        column: ColumnInspection,
        suggestion: PatternSuggestion,
        ctx: PlanContext,
    ) -> tuple[SqlType, Callable[[], Any | None]]:
        """Compile a per-column generator to remove planning work from the hot row loop."""
        pattern_id = suggestion.pattern_id or self._pattern_key_for_strategy(suggestion.strategy)
        if pattern_id and ctx.patterns.exists(pattern_id):
            choices = ctx.patterns.get_choices(pattern_id)
        else:
            choices = ["A", "B", "C", "D", "E", "F"]

        max_len = column.length
        if max_len is not None and max_len <= 0:
            max_len = None

        field_def = TextFieldDefinition(
            allow_null=column.nullable,
            fixed_length=None,
            min_length=0,
            max_length=max_len,
        )

        gen = TextGenerator(ctx.rng, choices, field_def)
        return (SqlType.STRING, gen.generate)

    def plan(
        self,
        column: ColumnInspection,
        suggestion: PatternSuggestion,
        ctx: PlanContext,
    ) -> ColumnEmitDefinition | None:
        # Pick a pattern name based on strategy; keep it dead simple for v0.1
        # If you don’t have pattern files yet, we fall back to a tiny in-memory pattern.
        pattern_id = suggestion.pattern_id or self._pattern_key_for_strategy(suggestion.strategy)
        if pattern_id and ctx.patterns.exists(pattern_id):
            choices = ctx.patterns.get_choices(pattern_id)
        else:
            # Fallback: minimal pattern so you can keep moving
            choices = ["A", "B", "C", "D", "E", "F"]

        max_len = column.length
        if max_len is not None and max_len <= 0:
            max_len = None

        # IMPORTANT: allow_null must match column nullability
        field_def = TextFieldDefinition(
            allow_null=column.nullable,
            fixed_length=None,
            min_length=0,
            max_length=max_len,
        )

        value = TextGenerator(ctx.rng, choices, field_def).generate()
        if value is None:
            return None  # nullable column -> skip emits, emitter will omit column/value

        return ColumnEmitDefinition(
            name=column.name,
            data_type=SqlType.STRING,
            value=value,
        )

    @staticmethod
    def _pattern_key_for_strategy(strategy: str) -> str | None:
        s = (strategy or "").strip().lower()
        # Your built-in suggestors produce strategy like "email"
        if s == "email":
            return "emails"
        elif s == "first_name":
            return "first_names"
        # You can expand this later:
        # if s == "severity": return "severity"
        return None
