from __future__ import annotations

from typing import Any, Protocol

from data_farm.l1_application.ports.inspector import Inspector


class InspectorFactory(Protocol):
    def create(self, config_data: dict[str, Any]) -> Inspector:
        """Create an inspector for the supplied data source config."""
        ...
