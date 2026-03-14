from __future__ import annotations

import random
from dataclasses import dataclass

from data_farm.l1_application.ports.pattern_source import PatternSource


@dataclass(slots=True)
class PlanContext:
    rng: random.Random
    patterns: PatternSource
    rows_per_table: int
