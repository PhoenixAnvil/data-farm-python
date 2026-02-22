import logging
from argparse import Namespace
from typing import cast

from data_farm.app.bootstrap import boot_app_from_ns
from data_farm.cli.base import InspectNamespace, ProjectNamespace
from data_farm.cli.handle_inspect import handle_inspect
from data_farm.cli.handle_project import handle_project
from data_farm.logging.logging import timed

logger = logging.getLogger("dfarm")


def dispatch(ns: Namespace) -> None:
    """Dispatch CLI argument processing."""

    ctx = boot_app_from_ns(ns)
    if ns.command == "project":
        pns = cast(ProjectNamespace, ns)
        with timed(logger, "Dispatching project"):
            handle_project(ctx, pns)
    elif ns.command == "inspect":
        ins = cast(InspectNamespace, ns)
        with timed(logger, "Dispatching inspect"):
            handle_inspect(ctx, ins)
