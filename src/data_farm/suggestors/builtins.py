# data_farm/suggestors/builtins.py
from __future__ import annotations

import re

from data_farm.models.models import ColumnInspection, PatternSuggestion
from data_farm.suggestors.base import PatternSuggestor
from data_farm.utils.enums import SqlType


def _mk(
    *,
    strategy: str,
    pattern_id: str | None,
    confidence: float,
    reason: str,
    suggestor: PatternSuggestor,
) -> PatternSuggestion:
    # Clamp confidence to [0, 1]
    c = max(0.0, min(1.0, confidence))
    return PatternSuggestion(
        strategy=strategy,
        pattern_id=pattern_id,
        confidence=c,
        reason=reason,
        suggestor=suggestor.name,
        priority=suggestor.priority,
    )


class EmailSuggestor(PatternSuggestor):
    name = "email"
    priority = 100

    def suggest(self, col: ColumnInspection) -> PatternSuggestion | None:
        n = col.name.lower()
        if "email" in n or re.search(r"\b(e_mail|emailaddr|email_address)\b", n):
            return _mk(
                strategy="email",
                pattern_id="email",
                confidence=0.95,
                reason="column name suggests email address",
                suggestor=self,
            )
        return None


class UuidSuggestor(PatternSuggestor):
    name = "uuid"
    priority = 90

    def suggest(self, col: ColumnInspection) -> PatternSuggestion | None:
        n = col.name.lower()
        t = col.data_type.name

        # Common UUID column names
        if n.endswith("_uuid") or n == "uuid" or "guid" in n:
            return _mk(
                strategy="uuid",
                pattern_id="uuid",
                confidence=0.95,
                reason="column name suggests UUID/GUID",
                suggestor=self,
            )

        # Type-based clue: PostgreSQL UUID type often stringifies to "UUID"
        if t == "UUID":
            return _mk(
                strategy="uuid",
                pattern_id="uuid",
                confidence=0.90,
                reason="column type is UUID",
                suggestor=self,
            )

        return None


class TimestampSuggestor(PatternSuggestor):
    name = "timestamp"
    priority = 80

    def suggest(self, col: ColumnInspection) -> PatternSuggestion | None:
        n = col.name.lower()
        t = col.data_type.name

        if any(k in n for k in ("created", "updated", "modified", "timestamp", "_at")):
            if "DATE" in t or "TIME" in t:
                return _mk(
                    strategy="datetime_recent",
                    pattern_id="datetime_recent",
                    confidence=0.90,
                    reason="name + type suggest datetime/timestamp",
                    suggestor=self,
                )
            return _mk(
                strategy="datetime_recent",
                pattern_id="datetime_recent",
                confidence=0.70,
                reason="column name suggests datetime; type not obviously datetime",
                suggestor=self,
            )

        return None


class StatusCodeSuggestor(PatternSuggestor):
    name = "status_code"
    priority = 70

    def suggest(self, col: ColumnInspection) -> PatternSuggestion | None:
        n = col.name.lower()

        # Common enterprise-ish naming
        if not any(k in n for k in ("status", "state", "type", "category", "code")):
            return None

        t = col.data_type.name

        # Strings are common for these fields
        if any(k == t for k in (SqlType.TEXT, SqlType.STRING, SqlType.FIXED_STRING)):
            return _mk(
                strategy="choice_pool",
                pattern_id="choice_pool",
                confidence=0.70,
                reason="name suggests status/type/code; use a choice pool",
                suggestor=self,
            )

        return None


class ForeignKeySuggestor(PatternSuggestor):
    name = "foreign_key"
    priority = 110  # FK should generally beat name-based guesses

    def suggest(self, col: ColumnInspection) -> PatternSuggestion | None:
        if not col.is_foreign_key:
            return None

        # Example: strategy indicates we should draw values from referenced table
        ref_table = None
        if col.foreign_key:
            ref_table = col.foreign_key.get("referred_table")

        reason = "column is a foreign key"
        if ref_table:
            reason = f"column is a foreign key to '{ref_table}'"

        return _mk(
            strategy="fk_reference",
            pattern_id="fk_reference",
            confidence=0.98,
            reason=reason,
            suggestor=self,
        )


class FirstNameSuggestor(PatternSuggestor):
    name = "first_name"
    priority = 100

    def suggest(self, col: ColumnInspection) -> PatternSuggestion | None:
        n = col.name.lower()
        if "first_name" in n or re.search(r"\b(first*name)\b", n):
            return _mk(
                strategy="string",
                pattern_id="first_names",
                confidence=0.95,
                reason="column name suggests first names",
                suggestor=self,
            )
        return None
