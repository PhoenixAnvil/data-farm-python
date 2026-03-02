from __future__ import annotations

from pathlib import Path
from typing import Protocol

from data_farm.domain.ports.pattern_source import PatternSource


class PatternSourceFactory(Protocol):
    def from_project(self, project_dir: Path) -> PatternSource: ...
