from argparse import Namespace
from pathlib import Path
from typing import cast

from data_farm.app.bootstrap import boot_app_from_ns
from data_farm.app.logging_config import setup_logging
from data_farm.cli.base import InspectNamespace, ProjectNamespace
from data_farm.cli.handle_inspect import handle_inspect
from data_farm.cli.handle_project import handle_project
from data_farm.logging.logging import generate_log_file_name


def dispatch(ns: Namespace) -> None:
    """Dispatch CLI argument processing."""

    ctx = boot_app_from_ns(ns)

    log_file = ns.log_file
    if log_file is not None:
        log_file = Path(log_file)
        if log_file == Path("."):
            log_file = generate_log_file_name()
        setup_logging(verbosity=ns.verbose, log_file=str(log_file))

    if ns.command == "project":
        pns = cast(ProjectNamespace, ns)
        handle_project(ctx, pns)
    elif ns.command == "inspect":
        ins = cast(InspectNamespace, ns)
        handle_inspect(ctx, ins)
