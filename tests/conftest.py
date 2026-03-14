from __future__ import annotations

import logging
import random
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

import pytest

from data_farm.l0_domain.enums import SqlType
from data_farm.l0_domain.model.models import ColumnInspection, NormalizedColumnType
from data_farm.l0_domain.ports.pattern_source import PatternSource
from data_farm.l1_application.plan.context import PlanContext


@dataclass(frozen=True)
class FakePatternSource(PatternSource):
    choices_by_id: Mapping[str, Sequence[str]]

    def get_choices(self, pattern_name: str) -> list[str]:
        return list(self.choices_by_id.get(pattern_name, []))

    def _load_pattern_file(self, key: str) -> list[str]:
        return ["Bob", "Alice", "Frank"]

    def exists(self, pattern_name: str) -> bool:
        return True

    def _pattern_path(self, key: str) -> Path:
        return Path(f"/fake/path/{key}.pat")

    @staticmethod
    def _norm_key(name: str) -> str:
        return name.lower().replace(" ", "_")


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
def pattern_source() -> PatternSource:
    return FakePatternSource(
        choices_by_id={
            "first_names": ["Alice", "Bob", "Charlie"],
            "email": ["a@example.com", "b@example.com"],
            "status": ["NEW", "OPEN", "CLOSED"],
        }
    )


@pytest.fixture()
def plan_context(rng_seeded: random.Random, pattern_source: PatternSource) -> PlanContext:
    return PlanContext(rng=rng_seeded, patterns=pattern_source, rows_per_table=3)


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
