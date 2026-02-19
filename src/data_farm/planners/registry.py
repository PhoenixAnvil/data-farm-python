from __future__ import annotations

from dataclasses import dataclass

from data_farm.messages.messages import msg
from data_farm.planners.boolean_planner import BooleanPlanner
from data_farm.planners.int_planner import IntPlanner
from data_farm.planners.numeric_planner import NumericPlanner
from data_farm.planners.protocols import ColumnPlanner
from data_farm.planners.string_planner import StringPlanner
from data_farm.planners.uuid_planner import UUIDPlanner


@dataclass(slots=True)
class PlannerRegistry:
    _by_strategy: dict[str, ColumnPlanner]

    def register(self, planner: ColumnPlanner, *aliases: str) -> None:
        keys = [planner.strategy, *aliases]
        for k in keys:
            key = k.strip().lower()
            if not key:
                raise ValueError(msg("err.planner.empty_strategy"))
            if key in self._by_strategy:
                raise ValueError(msg("err.planner.already_registered", planner=key))
            self._by_strategy[key] = planner

    def get(self, strategy: str) -> ColumnPlanner | None:
        return self._by_strategy.get(strategy.strip().lower())

    @classmethod
    def empty(cls) -> PlannerRegistry:
        return cls({})

    @classmethod
    def default(cls) -> PlannerRegistry:
        reg = cls.empty()

        reg.register(StringPlanner(), "string_short", "email")  # email uses StringPlanner for now
        reg.register(IntPlanner(), "int_age", "int_count")
        reg.register(BooleanPlanner())
        reg.register(NumericPlanner())
        reg.register(UUIDPlanner())
        return reg
