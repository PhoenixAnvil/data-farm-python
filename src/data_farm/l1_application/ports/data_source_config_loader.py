from __future__ import annotations

from pathlib import Path
from typing import Any, Protocol


class DataSourceConfigLoader(Protocol):
    def load(self, config_path: Path) -> list[dict[str, Any]]:
        """Load a data source config from the given path."""
        ...
