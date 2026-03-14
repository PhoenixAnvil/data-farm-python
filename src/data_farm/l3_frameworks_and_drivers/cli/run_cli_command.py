from __future__ import annotations

import logging
from argparse import Namespace
from dataclasses import dataclass
from typing import cast

from data_farm.l1_application.context import AppContext
from data_farm.l1_application.use_cases.inspect_use_case import run_inspect
from data_farm.l1_application.use_cases.project_use_case import run_project
from data_farm.l3_frameworks_and_drivers.cli.base import InspectNamespace, ProjectNamespace
from data_farm.l3_frameworks_and_drivers.cli.mappers.inspect_mapper import to_inspect_command
from data_farm.l3_frameworks_and_drivers.cli.mappers.project_mapper import to_project_command

logger = logging.getLogger("dfarm")


@dataclass(slots=True)
class UseCaseResult:
    exit_code: int = 0


def run_cli_command(ctx: AppContext, ns: Namespace) -> UseCaseResult:
    """
    Application-layer entry point for running a parsed CLI command.

    This is the seam where we'll later replace cli.handle_* calls with
    true application orchestration (DDD).
    """

    if ns.command == "project":
        project_ns = cast(ProjectNamespace, ns)
        project_cmd = to_project_command(project_ns)
        return UseCaseResult(run_project(ctx, project_cmd))

    if ns.command == "inspect":
        inspect_ns = cast(InspectNamespace, ns)
        inspect_cmd = to_inspect_command(inspect_ns)
        return UseCaseResult(run_inspect(ctx, inspect_cmd))

    # Unknown / missing command
    return UseCaseResult(2)
