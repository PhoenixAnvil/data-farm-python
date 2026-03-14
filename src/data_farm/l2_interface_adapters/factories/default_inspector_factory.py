from __future__ import annotations

from typing import Any

from data_farm.l1_application.ports.inspector import Inspector
from data_farm.l1_application.ports.inspector_factory import InspectorFactory
from data_farm.l2_interface_adapters.factories.inspector_registry import create_inspector


class DefaultInspectorFactory(InspectorFactory):
    def create(self, config_data: dict[str, Any]) -> Inspector:
        return create_inspector(config_data)
