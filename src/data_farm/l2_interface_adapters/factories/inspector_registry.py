from __future__ import annotations

from typing import Any

from data_farm.l1_application.ports.inspector import Inspector
from data_farm.l2_interface_adapters.inspection.database_inspector import DatabaseInspector

INSPECTOR_REGISTRY: dict[str, type[Inspector]] = {
    "database": DatabaseInspector,
}


def create_inspector(config: dict[str, Any]) -> Inspector:
    source_type = config["source_type"]

    try:
        inspector_cls = INSPECTOR_REGISTRY[source_type]
    except KeyError as err:
        raise ValueError(f"Unsupported source type: {source_type}.") from err

    return inspector_cls(config)
