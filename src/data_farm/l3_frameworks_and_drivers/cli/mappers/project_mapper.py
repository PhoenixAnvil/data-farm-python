from __future__ import annotations

from data_farm.l1_application.commands.project_command import ProjectCommand
from data_farm.l3_frameworks_and_drivers.cli.base import ProjectNamespace


def to_project_command(ns: ProjectNamespace) -> ProjectCommand:
    return ProjectCommand(
        projects_root=ns.projects_root,
        init=ns.init,
    )
