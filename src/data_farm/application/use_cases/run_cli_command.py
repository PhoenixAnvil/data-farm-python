from __future__ import annotations

import logging
from argparse import Namespace
from dataclasses import dataclass
from typing import cast

from data_farm.application.use_cases.inspect_use_case import run_inspect
from data_farm.application.use_cases.project_use_case import run_project
from data_farm.cli.base import AppContext, InspectNamespace, ProjectNamespace

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
        return UseCaseResult(run_project(ctx, cast(ProjectNamespace, ns)))

    if ns.command == "inspect":
        return UseCaseResult(run_inspect(ctx, cast(InspectNamespace, ns)))

    # Unknown / missing command
    return UseCaseResult(2)
