from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import tomli_w
from platformdirs import user_data_path

from data_farm.l1_application.ports.project_initializer import ProjectInitializer
from data_farm.l2_interface_adapters.config.default_data_farm_config_loader import (
    load_data_farm_config,
)
from data_farm.utils.config import default_data_source_config


class DefaultProjectInitializer(ProjectInitializer):
    def resolve_target(self, value: str, *, config_path: Path) -> Path:
        cd = load_data_farm_config(config_path)
        projects_root = self._get_projects_root(cd)
        return self._resolve_target(value, projects_root=projects_root, cwd=Path.cwd())

    def initialize(self, path: Path, *, force: bool = False) -> None:
        self._create_project_structure(path, force=force)

    def _get_projects_root(self, cd: Mapping[str, Any] | None) -> Path:
        if cd is None:
            return user_data_path("data_farm", appauthor=False) / "projects"
        proj = cd.get("project", {})
        root = proj.get("projects_root")
        return Path(root) if root else user_data_path("data_farm", appauthor=False) / "projects"

    def _resolve_target(self, value: str, projects_root: Path, cwd: Path) -> Path:
        p = Path(value)

        if p.is_absolute():
            return p

        if p.parent != Path("."):
            return (cwd / p).resolve()

        return (projects_root / p).resolve()

    # ruff: noqa: PLR0915
    def _create_project_structure(self, path: Path, *, force: bool = False) -> None:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        if not path.is_dir():
            raise NotADirectoryError(f"Project path is not a directory: {path}")

        if not force:
            try:
                next(path.iterdir())
            except StopIteration:
                pass
            else:
                raise FileExistsError(f"Refusing to initialize into non-empty directory: {path}. " "Use --force to proceed.")

        (path / "patterns").mkdir(exist_ok=True)
        (path / "output").mkdir(exist_ok=True)
        (path / "logs").mkdir(exist_ok=True)

        config = path / "data_source_config.toml"
        if config.exists() and not force:
            raise FileExistsError(f"Config already exists: {config}. Use --force to overwrite.")

        with config.open("wb") as f:
            tomli_w.dump(default_data_source_config, f)
