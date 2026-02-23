from __future__ import annotations

from argparse import ArgumentParser
from typing import Any, Protocol

from data_farm.messages.messages import msg


class SubParsers(Protocol):
    def add_parser(self, name: str, **kwargs: Any) -> ArgumentParser: ...


def build_project_parser(subparsers: SubParsers) -> None:
    project = subparsers.add_parser("project", help=msg("cli.help.prj.manage"))
    project.add_argument(
        "-r",
        "--projects-root",
        required=False,
        help=msg("cli.help.prj.set_root"),
    )
    project.add_argument("-i", "--init", required=False, help=msg("cli.help.prj.init"))
