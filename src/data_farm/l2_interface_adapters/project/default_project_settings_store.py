from __future__ import annotations

from pathlib import Path
from typing import Any

from data_farm.l1_application.ports.project_settings_store import ProjectSettingsStore
from data_farm.l2_interface_adapters.config.default_data_farm_config_loader import load_data_farm_config
from data_farm.utils.config import data_farm_config, store_data_farm_config

ConfigDict = dict[str, Any]


class DefaultProjectSettingsStore(ProjectSettingsStore):
    def set_projects_root(self, config_path: Path, projects_root: str) -> None:
        cd = load_data_farm_config(config_path) or dict(data_farm_config)
        cd.setdefault("project", {})["projects_root"] = projects_root
        store_data_farm_config(config_path, cd)
