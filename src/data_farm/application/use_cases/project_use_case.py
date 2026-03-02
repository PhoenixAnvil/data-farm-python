from __future__ import annotations

from data_farm.cli.base import AppContext, ProjectNamespace
from data_farm.cli.handle_project import handle_project


def run_project(app_ctx: AppContext, ns: ProjectNamespace) -> int:
    """Use case: manage project config/state. Delegates for now."""
    handle_project(app_ctx, ns)
    return 0
