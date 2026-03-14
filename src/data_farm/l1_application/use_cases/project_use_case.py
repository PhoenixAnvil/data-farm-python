from __future__ import annotations

from data_farm.l1_application.commands.project_command import ProjectCommand
from data_farm.l1_application.context import AppContext
from data_farm.l1_application.project_workflow import run_project_workflow


def run_project(app_ctx: AppContext, cmd: ProjectCommand) -> int:
    """Use case: manage project config/state. Delegates for now."""
    run_project_workflow(app_ctx, cmd)
    return 0
