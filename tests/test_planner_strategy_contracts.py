from __future__ import annotations

from data_farm.planners.registry import PlannerRegistry


def test_planner_registry_returns_planner_for_string() -> None:
    reg = PlannerRegistry.default()
    p = reg.get("string")
    assert p is not None


def test_planner_registry_unknown_strategy_returns_none() -> None:
    reg = PlannerRegistry.default()
    assert reg.get("nope") is None


def test_planner_registry_all_has_expected_core_strategies() -> None:
    reg = PlannerRegistry.default()
    strategies = reg.all().keys()
    # Keep this loose: just assert the ones you rely on exist.
    assert "string" in strategies
