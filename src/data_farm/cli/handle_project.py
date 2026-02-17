from pathlib import Path

import tomli_w
from platformdirs import user_data_path

from data_farm.app.bootstrap import load_data_farm_config
from data_farm.cli.base import AppContext, ProjectNamespace
from data_farm.utils.config import data_farm_config, default_data_source_config, store_data_farm_config


def handle_project(ctx: AppContext, ns: ProjectNamespace) -> None:
    if ns.projects_root:
        # Set Data Farm projects root directory.
        cd = load_data_farm_config(ctx.config_path) or data_farm_config
        cd["project"]["projects_root"] = ns.projects_root
        store_data_farm_config(ctx.config_path, cd)

    if ns.init:
        # Create a new Data Farm project structure.
        cd = load_data_farm_config(ctx.config_path) or data_farm_config
        pr = Path(cd.get("project", {}).get("projects_root", (user_data_path("data_farm", appauthor=False) / "projects")))
        pr.mkdir(parents=True, exist_ok=True)

        np = Path(ns.init)
        if len(np.parts) == 1:
            Path(pr / ns.init).mkdir(parents=True, exist_ok=True)
            create_project_structure(pr / ns.init)

        elif Path(ns.init).is_absolute() or Path(ns.init).parent == Path("."):
            Path(ns.init).mkdir(parents=True, exist_ok=True)
            create_project_structure(Path(ns.init))


def resolve_target(value: str, projects_root: Path) -> Path:
    p = Path(value)

    if p.is_absolute():
        return p

    if p.parent != Path("."):
        return (Path.cwd() / p).resolve()

    return (projects_root / p).resolve()


def create_project_structure(path: Path) -> None:
    p = Path(path)
    if p.exists() and p.is_dir():
        # Create structure directories
        patterns = p / "patterns"
        patterns.mkdir(parents=True, exist_ok=True)

        output = p / "output"
        output.mkdir(parents=True, exist_ok=True)

        logs = p / "logs"
        logs.mkdir(parents=True, exist_ok=True)

        config = p / "data_source_config.toml"
        with config.open("wb") as f:
            tomli_w.dump(default_data_source_config, f)
