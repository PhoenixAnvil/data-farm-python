from __future__ import annotations

import copy
import random
from pathlib import Path
from typing import Any

from data_farm.l1_application.commands.project_command import ProjectCommand
from data_farm.l1_application.context import AppContext
from data_farm.l1_application.use_cases.project_use_case import run_project
from data_farm.l2_interface_adapters.config.default_data_source_config_loader import (
    DefaultDataSourceConfigLoader,
)
from data_farm.l2_interface_adapters.factories.default_inspector_factory import (
    DefaultInspectorFactory,
)
from data_farm.l2_interface_adapters.patterns.filesystem_pattern_source_factory import (
    FilesystemPatternSourceFactory,
)
from data_farm.l2_interface_adapters.project.default_project_initializer import (
    DefaultProjectInitializer,
)
from data_farm.l2_interface_adapters.project.default_project_settings_store import (
    DefaultProjectSettingsStore,
)


def test_run_project_init_creates_structure(tmp_path: Path) -> None:
    app_config_path = tmp_path / "app.toml"
    projects_root = tmp_path / "projects"

    with app_config_path.open("a", encoding="utf-8") as f:
        f.write("[project]\n")
        f.write(f"projects_root = '{projects_root}'\n")

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
        pattern_source_factory=FilesystemPatternSourceFactory(),
        inspector_factory=DefaultInspectorFactory(),
        data_source_config_loader=DefaultDataSourceConfigLoader(),
        project_initializer=DefaultProjectInitializer(),
        project_settings_store=DefaultProjectSettingsStore(),
    )

    cmd = ProjectCommand(init="my_proj")

    run_project(ctx, cmd)

    proj_dir = projects_root / "my_proj"
    assert (proj_dir / "patterns").is_dir()
    assert (proj_dir / "output").is_dir()
    assert (proj_dir / "logs").is_dir()
    assert (proj_dir / "data_source_config.toml").is_file()


def test_run_project_projects_root_writes_projects_root_when_cmd_projects_root_set(
    tmp_path: Path,
) -> None:
    app_config_path = tmp_path / "app.toml"

    saved: dict[str, Any] = {}

    class FakeProjectSettingsStore(DefaultProjectSettingsStore):
        def set_projects_root(self, config_path: Path, projects_root: str) -> None:
            saved.clear()
            saved.update({"project": {"projects_root": projects_root}})

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
        pattern_source_factory=FilesystemPatternSourceFactory(),
        inspector_factory=DefaultInspectorFactory(),
        data_source_config_loader=DefaultDataSourceConfigLoader(),
        project_initializer=DefaultProjectInitializer(),
        project_settings_store=FakeProjectSettingsStore(),
    )

    cmd = ProjectCommand(projects_root=str(tmp_path / "projects"))

    run_project(ctx, cmd)

    assert saved["project"]["projects_root"] == str(tmp_path / "projects")


def test_run_project_projects_root_preserves_existing_config_keys_when_writing_projects_root(
    tmp_path: Path,
) -> None:
    app_config_path = tmp_path / "app.toml"

    saved: dict[str, Any] = {
        "test": "not removed",
        "project": {"test": "not removed"},
    }

    class FakeProjectSettingsStore(DefaultProjectSettingsStore):
        def set_projects_root(self, config_path: Path, projects_root: str) -> None:
            current = copy.deepcopy(saved)
            current.setdefault("project", {})["projects_root"] = projects_root
            saved.clear()
            saved.update(current)

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
        pattern_source_factory=FilesystemPatternSourceFactory(),
        inspector_factory=DefaultInspectorFactory(),
        data_source_config_loader=DefaultDataSourceConfigLoader(),
        project_initializer=DefaultProjectInitializer(),
        project_settings_store=FakeProjectSettingsStore(),
    )

    cmd = ProjectCommand(projects_root=str(tmp_path / "projects"))

    run_project(ctx, cmd)

    assert saved["test"] == "not removed"
    assert saved["project"]["test"] == "not removed"
    assert saved["project"]["projects_root"] == str(tmp_path / "projects")
