# data_farm/suggestors/model.py
from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Any

from data_farm.utils.enums import SqlType


@dataclass(frozen=True, slots=True)
class TableInspection:
    """TBD"""

    table: str
    schema: str | None
    columns: list[ColumnInspection]
    row_count: int


@dataclass(frozen=True, slots=True)
class ColumnInspection:
    """
    Normalized, DB-agnostic view of a column.
    Keep this stable so plugins never depend on SQLAlchemy.
    """

    table: str
    name: str
    data_type: NormalizedColumnType  # normalized string (e.g., "VARCHAR", "INTEGER")
    nullable: bool
    length: int | None = None
    default: Any | None = None
    autoincrement: bool | None = None
    is_primary_key: bool = False
    is_foreign_key: bool = False
    foreign_key: dict[str, Any] | None = None
    comment: str | None = None


@dataclass(frozen=True)
class PatternSuggestion:
    """
    A plugin's suggestion for how to generate data for a column.
    """

    strategy: str  # e.g. "email", "uuid", "full_name"
    confidence: float  # 0.0 to 1.0
    reason: str  # human explanation (great for debugging/logging)
    suggestor: str  # plugin name
    priority: int  # tie-breaker (higher wins)
    pattern_id: str | None = None


@dataclass(frozen=True, slots=True)
class ColumnEmitDefinition:
    """
    Emit an INSERT statement based on these values.
    """

    name: str
    data_type: SqlType
    value: str


@dataclass(frozen=True, slots=True)
class NormalizedColumnType:
    """Normalized column SQL data type."""

    name: SqlType
    length: int | None
    num_precision: int | None
    scale: int | None
    time_precision: int | None


@dataclass(frozen=True)
class AppConfig:
    """Data Farm Global Configuration."""

    config_root: str
    data_root: str
    config_path: str
    config_data: dict[str, Any]
    rng: random.Random
