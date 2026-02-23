"""Dispatch application work based on parsed CLI arguments.

This module receives an argparse namespace, boots the application context, and
dispatches to the appropriate handler.

Responsibilities:
- Build :class:`~data_farm.cli.base.AppContext` via bootstrap
- Route to subcommand handlers

This module does not:
- Parse arguments (argparse does that)
- Implement pipeline work directly
"""

import logging
import sys
from argparse import ArgumentParser, Namespace
from typing import cast

from data_farm.app.bootstrap import boot_app_from_ns
from data_farm.cli.base import InspectNamespace, ProjectNamespace
from data_farm.cli.handle_inspect import handle_inspect
from data_farm.cli.handle_project import handle_project
from data_farm.logging.logging import timed

logger = logging.getLogger("dfarm")


def dispatch(parser: ArgumentParser, ns: Namespace) -> None:
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
    else:
        parser.print_help()
        sys.exit(3)
