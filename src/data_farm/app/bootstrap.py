from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from data_farm.cli.base import AppContext
from data_farm.utils.config import (
    app_config_file_exists,
    config_dir_exists,
    data_dir_exists,
    data_farm_config,
    data_farm_config_path,
    data_farm_config_root,
    data_farm_data_root,
    data_farm_logs_dir,
    load_data_farm_config,
    make_data_farm_config_dir,
    make_data_farm_data_dir,
    store_data_farm_config,
)
from data_farm.utils.random import create_rng


def boot_app_from_ns(ns: Namespace) -> AppContext:
    cr = getattr(ns, "config_dir", data_farm_config_root)
    dr = getattr(ns, "data_dir", data_farm_data_root)
    cp = getattr(ns, "config_path", data_farm_config_path)
    logs_dir = getattr(ns, "logs_dir", data_farm_logs_dir)
    seed = getattr(ns, "seed", None)
    dcd = data_farm_config

    if not config_dir_exists(cr):
        make_data_farm_config_dir(cr)

    if not data_dir_exists(dr):
        make_data_farm_data_dir(dr)

    if not app_config_file_exists(cp):
        store_data_farm_config(cp, dcd)

    cd = load_data_farm_config(cp)

    default_seed = "rng-global-default-seed-v0.1.0"
    seed_value = seed or (cd.get("seed", default_seed) if cd else default_seed)
    rng = create_rng(seed_value)

    debug = getattr(ns, "debug", False)

    return AppContext(
        config_dir=cr,
        data_dir=dr,
        config_path=cp,
        config_data=cd,
        seed=seed,
        rng=rng,
        projects_root=Path(cd.get("project", {}).get("projects_root", Path(dr) / "projects")),
        max_generation=cd.get("limits", {}).get("max_generation", 1000000),
        logs_dir=logs_dir,
        debug=debug,
    )
