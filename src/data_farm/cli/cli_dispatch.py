from argparse import Namespace
from typing import cast

from data_farm.app.bootstrap import boot_app_from_ns
from data_farm.app.logging_config import setup_logging
from data_farm.cli.base import AppNamespace, InspectNamespace, ProjectNamespace
from data_farm.cli.handle_inspect import handle_inspect
from data_farm.cli.handle_project import handle_project


def dispatch(ns: Namespace) -> None:
    """Dispatch CLI argument processing."""

    ctx = boot_app_from_ns(ns)
    setup_logging(verbosity=ns.verbose, log_file=ns.log_file)
    if ns.command == "app":
        ans = cast(AppNamespace, ns)
        # Do we even need this?
    if ns.command == "project":
        pns = cast(ProjectNamespace, ns)
        handle_project(ctx, pns)
    elif ns.command == "inspect":
        ins = cast(InspectNamespace, ns)
        handle_inspect(ctx, ins)
