from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectCommand:
    projects_root: str | None = None
    init: str | None = None
