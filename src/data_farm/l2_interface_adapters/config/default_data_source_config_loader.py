from __future__ import annotations

from pathlib import Path
from typing import Any

from data_farm.l1_application.ports.data_source_config_loader import (
    DataSourceConfigLoader,
)
from data_farm.utils.config import load_data_source_config


class DefaultDataSourceConfigLoader(DataSourceConfigLoader):
    def load(self, config_path: Path) -> list[dict[str, Any]]:
        return load_data_source_config(config_path)
