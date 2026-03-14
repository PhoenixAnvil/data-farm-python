from __future__ import annotations

from pathlib import Path
from typing import Any

from data_farm.utils.config import load_data_farm_config as _load_data_farm_config

ConfigDict = dict[str, Any]


def load_data_farm_config(config_path: Path) -> ConfigDict | None:
    return _load_data_farm_config(config_path)
