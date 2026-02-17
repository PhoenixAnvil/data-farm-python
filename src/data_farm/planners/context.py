from __future__ import annotations

import random
from dataclasses import dataclass

from data_farm.patterns.registry import PatternRegistry  # adjust import


@dataclass(slots=True)
class PlanContext:
    rng: random.Random
    patterns: PatternRegistry
    rows_per_table: int
