"""Define the Data Farm CLI surface.

This module constructs the top-level argparse parser and defines the typed
contracts used by downstream layers (bootstrap/dispatch/handlers).

This module does not execute application work; it only defines the CLI shape.
"""

import argparse
from typing import Protocol

from data_farm.l3_frameworks_and_drivers.cli.app_parser import build_app_parser
from data_farm.l3_frameworks_and_drivers.cli.inspect_parser import build_inspect_parser
from data_farm.l3_frameworks_and_drivers.cli.project_parser import build_project_parser


# ruff: noqa: PLR0915
def build_parser() -> argparse.ArgumentParser:
    """
    Create and return the dfarm CLI parser.

    :return: Configured argparse parser for the dfarm CLI.
    :rtype: argparse.ArgumentParser
    """
    program_name = "dfarm"
    program_description = "Data Farm - A schema-aware test data generation tool"

    parser = argparse.ArgumentParser(
        prog=program_name,
        description=program_description,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    build_app_parser(parser)
    build_project_parser(subparsers)
    build_inspect_parser(subparsers)

    return parser


class InspectNamespace(Protocol):
    command: str
    project: str
    config: str
    seed: int | str
    table: str
    rows: int
    output_file: str
    schema: str
    insert_batch_size: int


class ProjectNamespace(Protocol):
    command: str
    projects_root: str | None
    init: str | None
