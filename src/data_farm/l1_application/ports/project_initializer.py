from __future__ import annotations

from pathlib import Path
from typing import Protocol


class ProjectInitializer(Protocol):
    def resolve_target(self, value: str, *, config_path: Path) -> Path: ...

    def initialize(self, path: Path, *, force: bool = False) -> None: ...
