from __future__ import annotations

from pathlib import Path
from typing import Protocol


class ProjectSettingsStore(Protocol):
    def set_projects_root(self, config_path: Path, projects_root: str) -> None: ...
