from __future__ import annotations

import random
from dataclasses import dataclass

from data_farm.domain.ports.pattern_source import PatternSource  # adjust import


@dataclass(slots=True)
class PlanContext:
    rng: random.Random
    patterns: PatternSource
    rows_per_table: int
