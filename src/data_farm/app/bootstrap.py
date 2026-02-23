"""Bootstrap Data Farm application state.

This module builds an :class:`~data_farm.cli.base.AppContext` by combining:
- Data Farm defaults
- A Data Farm configuration file (creating one on first run if needed)
- Command-line overrides

Bootstrap is responsible for lightweight setup only:
- Ensuring application directories exist
- Loading/storing configuration
- Creating the global RNG
- Configuring logging for the application

Bootstrap does not:
- Parse CLI arguments
- Execute pipeline work (inspect/suggest/plan/generate/emit)
- Perform heavy I/O beyond config and directory setup
"""

from __future__ import annotations

from argparse import Namespace
from pathlib import Path

from data_farm.app.logging_config import setup_logging
from data_farm.cli.base import AppContext
from data_farm.logging.logging import generate_log_file_name
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
    cr = ns.config_dir or data_farm_config_root
    dr = ns.data_dir or data_farm_data_root
    cp = ns.config_path or data_farm_config_path
    log_file = ns.log_file or data_farm_logs_dir
    seed = ns.seed
    dcd = data_farm_config

    validate_app_dirs(cr, dr)

    if not app_config_file_exists(cp):
        store_data_farm_config(cp, dcd)

    cd = load_data_farm_config(cp)

    default_seed = "rng-global-default-seed-v0.1.0"
    seed_value = seed or (cd.get("seed", default_seed) if cd else default_seed)
    rng = create_rng(seed_value)

    debug = getattr(ns, "debug", False)

    setup_logger(ns)

    return AppContext(
        config_dir=cr,
        data_dir=dr,
        config_path=cp,
        config_data=cd,
        seed=seed_value,
        rng=rng,
        projects_root=Path(cd.get("project", {}).get("projects_root", Path(dr) / "projects")),
        max_generation=cd.get("limits", {}).get("max_generation", 1000000),
        log_file=log_file,
        debug=debug,
    )


def validate_app_dirs(app_config_root: str, app_data_root: str) -> None:
    if not config_dir_exists(app_config_root):
        make_data_farm_config_dir(app_config_root)

    if not data_dir_exists(app_data_root):
        make_data_farm_data_dir(app_data_root)


# ruff: noqa: PLR0915
def setup_logger(ns: Namespace) -> None:
    """
    Configure logging for the application.

    Rules for --log-file:
      - not provided: console logging only
      - "." (or "./", ".\\"): auto-generate a file name in CWD
      - existing directory path: auto-generate a file name in that directory
      - otherwise: treat as a file path
    """
    log_file: str | None = None

    raw = getattr(ns, "log_file", None)
    if raw:
        raw_str = str(raw).strip()

        # Treat ".", "./", ".\\" as "current directory"
        if raw_str in {".", "./", ".\\"}:
            log_path = Path(generate_log_file_name())
            log_file = str(log_path)
        else:
            p = Path(raw_str).expanduser()

            # If they provided a directory, write an auto-named log file inside it.
            if p.exists() and p.is_dir():
                log_path = p / Path(generate_log_file_name()).name
                log_file = str(log_path)
            else:
                # Otherwise treat it as a file path (even if it doesn't exist yet).
                log_file = str(p)

    setup_logging(verbosity=ns.verbose, log_file=log_file)
