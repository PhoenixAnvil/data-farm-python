"""Handle `dfarm project` commands.

This module implements project-focused actions such as initialization and
listing. It is invoked by the CLI dispatch layer and uses the shared
application context.
"""

from __future__ import annotations

import logging
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomli_w
from platformdirs import user_data_path

from data_farm.application.bootstrap import load_data_farm_config
from data_farm.cli.base import AppContext, ProjectNamespace
from data_farm.utils.config import data_farm_config, default_data_source_config, store_data_farm_config

ConfigDict = dict[str, Any]


logger = logging.getLogger("dfarm")


@dataclass(frozen=True)
class ProjectDeps:
    load_config: Callable[[Path], ConfigDict | None]
    store_config: Callable[[Path, ConfigDict], None]
    default_projects_root: Callable[[], Path]
    cwd: Callable[[], Path]


def get_projects_root(cd: Mapping[str, Any] | None, deps: ProjectDeps) -> Path:
    if cd is None:
        return deps.default_projects_root()
    proj = cd.get("project", {})
    root = proj.get("projects_root")
    return Path(root) if root else deps.default_projects_root()


# ruff: noqa: PLR0915
def default_deps() -> ProjectDeps:
    return ProjectDeps(
        load_config=load_data_farm_config,
        store_config=store_data_farm_config,
        default_projects_root=lambda: user_data_path("data_farm", appauthor=False) / "projects",
        cwd=Path.cwd,
    )


def handle_project(ctx: AppContext, ns: ProjectNamespace, deps: ProjectDeps | None = None) -> None:
    deps = deps or default_deps()

    # 1) Apply projects_root setting (config write)
    if ns.projects_root:
        cd = deps.load_config(Path(ctx.config_path)) or dict(
            data_farm_config
        )  # shallow copy is fine if values are nested dicts you mutate
        cd.setdefault("project", {})["projects_root"] = ns.projects_root
        deps.store_config(Path(ctx.config_path), cd)

    # 2) Init a project structure (filesystem)
    if ns.init:
        cd = deps.load_config(Path(ctx.config_path)) or dict(data_farm_config)
        pr = get_projects_root(cd, deps)
        pr.mkdir(parents=True, exist_ok=True)

        target = _resolve_target(ns.init, projects_root=pr, cwd=deps.cwd())
        _create_project_structure(target)


def _resolve_target(value: str, projects_root: Path, cwd: Path) -> Path:
    p = Path(value)

    if p.is_absolute():
        return p

    if p.parent != Path("."):
        return (cwd / p).resolve()

    return (projects_root / p).resolve()


def _create_project_structure(path: Path, *, force: bool = False) -> None:
    # Convenience: create missing root folder
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)

    if not path.is_dir():
        raise NotADirectoryError(f"Project path is not a directory: {path}")

    # Safety: refuse to init into non-empty dirs unless forced
    if not force:
        try:
            next(path.iterdir())
        except StopIteration:
            pass  # empty dir => ok
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
