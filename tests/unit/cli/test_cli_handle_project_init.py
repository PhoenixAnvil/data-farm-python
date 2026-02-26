from __future__ import annotations

import copy
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from data_farm.cli.base import AppContext, ProjectNamespace
from data_farm.cli.handle_project import ProjectDeps, handle_project


@dataclass
class FakeProjectNs:
    command: str = "project"
    projects_root: str | None = None
    init: str | None = None


def test_handle_project_init_creates_structure(tmp_path: Path) -> None:
    # Arrange
    app_config_path = tmp_path / "app.toml"
    projects_root = tmp_path / "projects"

    def load(_path: Path) -> dict[str, Any]:
        return {"project": {"projects_root": str(projects_root)}}

    def store(_path: Path, _data: dict[str, Any]) -> None:
        return

    deps = ProjectDeps(
        load_config=load,
        store_config=store,
        default_projects_root=lambda: tmp_path / "default-projects",
        cwd=lambda: tmp_path,
    )

    ctx = AppContext(
        config_dir=str(tmp_path / "cfg"),
        data_dir=str(tmp_path / "data"),
        config_path=str(app_config_path),
        config_data={},
        seed="test-seed",
        rng=random.Random(123),
        projects_root=projects_root,
        max_generation=100,
        log_file="",
        debug=False,
    )

    ns: ProjectNamespace = FakeProjectNs(init="my_proj")

    # Act
    handle_project(ctx, ns, deps=deps)

    # Assert
    proj_dir = projects_root / "my_proj"
    assert (proj_dir / "patterns").is_dir()
    assert (proj_dir / "output").is_dir()
    assert (proj_dir / "logs").is_dir()
    assert (proj_dir / "data_source_config.toml").is_file()


def test_handle_project_projects_root_writes_projects_root_when_ns_projects_root_set(tmp_path: Path) -> None:
    app_config_path = tmp_path / "app.toml"

    # in-memory persisted config
    saved: dict[str, Any] = {}

    def load(_path: Path) -> dict[str, Any] | None:
        return saved or None

    def store(_path: Path, data: dict[str, Any]) -> None:
        saved.clear()
        saved.update(data)

    deps = ProjectDeps(
        load_config=load,
        store_config=store,
        default_projects_root=lambda: tmp_path / "default-projects",
        cwd=lambda: tmp_path,
    )

    ctx = AppContext(
        config_dir=str(tmp_path / "cfg"),
        data_dir=str(tmp_path / "data"),
        config_path=str(app_config_path),
        config_data={},
        seed="test-seed",
        rng=random.Random(123),
        projects_root=tmp_path / "whatever",
        max_generation=100,
        log_file="",
        debug=False,
    )

    ns: ProjectNamespace = FakeProjectNs(projects_root=str(tmp_path / "projects"), init=None)

    handle_project(ctx, ns, deps=deps)

    assert saved["project"]["projects_root"] == str(tmp_path / "projects")


def test_handle_project_projects_root_preserves_existing_config_keys_when_writing_projects_root(tmp_path: Path) -> None:
    app_config_path = tmp_path / "app.toml"

    # in-memory persisted config
    saved: dict[str, Any] = {
        "test": "not removed",
        "project": {"test": "not removed"},
    }

    def load(_path: Path) -> dict[str, Any] | None:
        return copy.deepcopy(saved)

    def store(_path: Path, data: dict[str, Any]) -> None:
        saved.clear()
        saved.update(data)

    deps = ProjectDeps(
        load_config=load,
        store_config=store,
        default_projects_root=lambda: tmp_path / "default-projects",
        cwd=lambda: tmp_path,
    )

    ctx = AppContext(
        config_dir=str(tmp_path / "cfg"),
        data_dir=str(tmp_path / "data"),
        config_path=str(app_config_path),
        config_data={},
        seed="test-seed",
        rng=random.Random(123),
        projects_root=tmp_path / "whatever",
        max_generation=100,
        log_file="",
        debug=False,
    )

    ns: ProjectNamespace = FakeProjectNs(projects_root=str(tmp_path / "projects"), init=None)

    handle_project(ctx, ns, deps=deps)

    assert saved["test"] == "not removed"
    assert saved["project"]["test"] == "not removed"
    assert saved["project"]["projects_root"] == str(tmp_path / "projects")
