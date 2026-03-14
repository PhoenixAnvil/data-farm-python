from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from data_farm.l1_application.ports.data_source_config_loader import DataSourceConfigLoader
from data_farm.l1_application.ports.inspector_factory import InspectorFactory
from data_farm.l1_application.ports.pattern_source_factory import PatternSourceFactory
from data_farm.l1_application.ports.project_initializer import ProjectInitializer
from data_farm.l1_application.ports.project_settings_store import ProjectSettingsStore


@dataclass(frozen=True)
class AppContext:
    config_dir: str
    data_dir: str
    config_path: str
    config_data: dict[str, Any]
    seed: str | int | None
    rng: random.Random
    projects_root: Path
    max_generation: int
    log_file: str
    debug: bool
    pattern_source_factory: PatternSourceFactory
    inspector_factory: InspectorFactory
    data_source_config_loader: DataSourceConfigLoader
    project_settings_store: ProjectSettingsStore
    project_initializer: ProjectInitializer
