from __future__ import annotations

import logging
import random
from collections.abc import Iterator
from pathlib import Path

import pytest

from data_farm.models.models import ColumnInspection, NormalizedColumnType
from data_farm.patterns.registry import PatternRegistry
from data_farm.planners.context import PlanContext
from data_farm.utils.enums import SqlType


@pytest.fixture()
def rng_seeded() -> random.Random:
    # Deterministic RNG for repeatable tests
    return random.Random(42)


@pytest.fixture()
def patterns_dir(tmp_path: Path) -> Path:
    d = tmp_path / "patterns"
    d.mkdir()
    # .pat files are line-based, comments start with '#'
    (d / "first_names.pat").write_text("Alice\nBob\n# comment\n\nCharlie\n", encoding="utf-8")
    (d / "email.pat").write_text("a@example.com\nb@example.com\n", encoding="utf-8")
    return d


@pytest.fixture()
def pattern_registry(patterns_dir: Path) -> PatternRegistry:
    return PatternRegistry(patterns_dir=patterns_dir)


@pytest.fixture()
def plan_context(rng_seeded: random.Random, pattern_registry: PatternRegistry) -> PlanContext:
    return PlanContext(rng=rng_seeded, patterns=pattern_registry, rows_per_table=3)


@pytest.fixture()
def col_first_name() -> ColumnInspection:
    return ColumnInspection(
        table="t1",
        name="first_name",
        data_type=NormalizedColumnType(
            name=SqlType.STRING,
            length=32,
            num_precision=None,
            scale=None,
            time_precision=None,
        ),
        nullable=False,
        length=32,
    )


@pytest.fixture()
def col_short_string() -> ColumnInspection:
    return ColumnInspection(
        table="t1",
        name="code",
        data_type=NormalizedColumnType(
            name=SqlType.STRING,
            length=8,
            num_precision=None,
            scale=None,
            time_precision=None,
        ),
        nullable=False,
        length=8,
    )


pytest_plugins = [
    "tests.helpers.factories",
]

LOGGER_NAME = "dfarm"


# ruff: noqa: PLR0915
@pytest.fixture()
def dfarm_logger() -> Iterator[logging.Logger]:
    """
    Yield a clean dfarm logger for unit tests.

    - Clears handlers and disables propagation.
    - Restores original handlers afterwards.
    """
    logger = logging.getLogger(LOGGER_NAME)
    old_handlers = list(logger.handlers)
    old_propagate = logger.propagate
    old_level = logger.level

    logger.handlers.clear()
    logger.propagate = False
    logger.setLevel(logging.DEBUG)

    try:
        yield logger
    finally:
        logger.handlers.clear()
        for h in old_handlers:
            logger.addHandler(h)
        logger.propagate = old_propagate
        logger.setLevel(old_level)


@pytest.fixture()
def tmp_log_base(tmp_path: Path) -> Path:
    # Base path used by setup_logging(log_file=...) which later derives .csv/.jsonl
    return tmp_path / "dfarm.log"
