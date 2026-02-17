"""
Command-line interface definition for dfarm.

This module defines the argparse parser and CLI contract for the tool.
"""

import argparse
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from data_farm.messages.messages import msg


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

    parser.add_argument("-v", "--verbose", action="count", default=0, help=msg("cli.help.global.verbose"))
    parser.add_argument("-l", "--log-file", type=str, help=msg("cli.help.global.log_file"))
    parser.add_argument("-d", "--debug", action="store_true", required=False, help=msg("cli.help.global.debug"))

    subparsers = parser.add_subparsers(dest="command", required=True)

    app = subparsers.add_parser("app", help=msg("cli.help.app"))
    app.add_argument("-c", "--config-dir", required=False, help=msg("cli.help.app.ovr_cfg_dir"))
    app.add_argument("-d", "--data-dir", required=False, help=msg("cli.help.app.ovr_data_dir"))
    app.add_argument("-p", "--config-path", required=False, help=msg("cli.help.app.ovr_cfg_path"))

    project = subparsers.add_parser("project", help=msg("cli.help.prj.manage"))
    project.add_argument(
        "-r",
        "--projects-root",
        required=False,
        help=msg("cli.help.prj.set_root"),
    )
    project.add_argument("-i", "--init", required=False, help=msg("cli.help.prj.init"))
    project.add_argument(
        "-l",
        "--list",
        action="store_true",
        required=False,
        help=msg("cli.help.prj.list"),
    )

    inspect = subparsers.add_parser("inspect", help=msg("cli.help.insp"))
    inspect.add_argument("-p", "--project", required=True, help=msg("cli.help.insp.project"))
    inspect.add_argument("-c", "--config", required=False, help=msg("cli.help.insp.config"))
    inspect.add_argument("-s", "--seed", required=False, help=msg("cli.help.insp.seed"))
    inspect.add_argument("-t", "--table", required=False, help=msg("cli.help.insp.table"))
    inspect.add_argument("-r", "--rows", required=False, help=msg("cli.help.insp.rows"))
    inspect.add_argument("-o", "--output-file", required=False, help=msg("cli.help.insp.out"))

    rng = subparsers.add_parser("rng", help=msg("cli.help.rng"))
    rng.add_argument("-s", "--seed", required=True, help=msg("cli.help.rng.seed"))

    return parser


@dataclass(frozen=True)
class InspectArgs:
    project: str
    config: str
    seed: int | str


@dataclass(frozen=True)
class ProjectArgs:
    projects_root: str
    init: str


@dataclass(frozen=True)
class AppContext:
    config_dir: str
    data_dir: str
    config_path: str
    config_data: dict[str, Any]
    seed: str | int | None
    rng: random.Random
    projects_root: Path
    max_generation: int
    logs_dir: str
    debug: bool


class InspectNamespace(Protocol):
    command: str
    project: str
    config: str
    seed: int | str
    table: str
    rows: int
    output_file: str
    logs_dir: str


class ProjectNamespace(Protocol):
    command: str
    projects_root: str
    init: str
    logs_dir: str


class AppNamespace(Protocol):
    command: str
    config_root: str
    data_root: str
    config_path: str
