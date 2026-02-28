from __future__ import annotations

import argparse

import pytest

from data_farm.cli.app_parser import build_app_parser
from data_farm.cli.inspect_parser import build_inspect_parser
from data_farm.cli.project_parser import build_project_parser


@pytest.mark.parametrize(
    "argv",
    [
        ["project", "--init", "test"],
    ],
)
def test_app_parser_parses_known_commands(argv: list[str]) -> None:
    parser = argparse.ArgumentParser(
        prog="Test",
        description="Test",
    )
    build_app_parser(parser)
    subparsers = parser.add_subparsers(dest="command", required=True)
    build_inspect_parser(subparsers)
    build_project_parser(subparsers)
    ns = parser.parse_args(argv)
    assert ns is not None
