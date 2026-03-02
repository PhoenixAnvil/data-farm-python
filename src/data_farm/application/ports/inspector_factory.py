from __future__ import annotations

from pathlib import Path
from typing import Protocol

from data_farm.schema.base import Inspector


class InspectorFactory(Protocol):
    def create(self, config_path: Path) -> Inspector: ...
