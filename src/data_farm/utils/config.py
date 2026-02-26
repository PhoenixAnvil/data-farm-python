""" """

import tomllib
from pathlib import Path
from typing import Any

import tomli_w
from platformdirs import user_config_dir, user_data_dir

from data_farm.messages.messages import msg
from data_farm.utils.path import FilePathValidator

data_farm_config_root = str(Path(user_config_dir("datafarm", appauthor=False)))
data_farm_data_root = str(Path(user_data_dir("datafarm", appauthor=False)))

data_farm_config_path = str(Path(data_farm_config_root) / "datafarm.toml")
data_farm_config: dict[str, Any] = {"project": {"projects_root": str(Path(data_farm_data_root) / "projects")}}

data_farm_logs_dir = str(Path(user_data_dir("datafarm", appauthor=False)) / "logs")


def load_data_source_config(config_path: Path | None = None) -> list[dict[str, Any]]:
    """TBD"""
    path = FilePathValidator(config_path).validate_path()
    with path.open("rb") as f:
        data: dict[str, Any] = tomllib.load(f)
        ds_config = data["data_source"]
        r_config = data["random"]
    validate_data_source_config(ds_config)
    validate_data_source_config(r_config)
    configs = [ds_config, r_config]
    return configs


default_data_source_config = {
    "seed": "",
    "source_type": "",
    "driver": "",
    "user_env_var": "",
    "password_env_var": "",
    "host": "",
    "port": "",
    "database": "",
}


def validate_data_source_config(config: dict[str, Any]) -> None:
    """Validate a given data source config file is valid."""
    if not config:
        raise ValueError(msg("err.utils.config.val_data_src_cfg"))


def load_data_farm_config(config_path: Path) -> dict[str, Any]:
    path = FilePathValidator(config_path).validate_path()
    with path.open("rb") as f:
        data: dict[str, Any] = tomllib.load(f)
        config = data
    validate_data_farm_config(config)
    return config


def validate_data_farm_config(config: dict[str, Any]) -> None:
    """Validate a given data farm config file is valid."""
    if not config:
        raise ValueError(msg("err.utils.config.val_data_src_cfg"))


def store_data_farm_config(config_path: Path, config: dict[str, Any]) -> None:
    validate_data_farm_config(config)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with config_path.open("wb") as f:
        tomli_w.dump(config, f)


def make_data_farm_data_dir(path: str) -> None:
    p = Path(path)
    if not p.exists():
        p.mkdir(parents=True, exist_ok=False)

    if not p.exists():
        raise ValueError(msg("err.utils.config.dir_create_fail", path=p))


def make_data_farm_config_dir(path: str) -> None:
    p = Path(path)
    if not p.exists():
        p.mkdir(parents=True, exist_ok=False)

    if not p.exists():
        raise ValueError(msg("err.utils.config.dir_create_fail", path=p))


def config_dir_exists(path: str) -> bool:
    p = Path(path)
    return p.exists()


def data_dir_exists(path: str) -> bool:
    p = Path(path)
    return p.exists()


def app_config_file_exists(path: str) -> bool:
    p = Path(path)
    return p.exists()


def data_source_config_file_exists(path: str) -> bool:
    p = Path(path)
    return p.exists()
