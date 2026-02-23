from __future__ import annotations

from argparse import ArgumentParser
from typing import Any, Protocol

from data_farm.messages.messages import msg


class SubParsers(Protocol):
    def add_parser(self, name: str, **kwargs: Any) -> ArgumentParser: ...


def build_inspect_parser(subparsers: SubParsers) -> None:
    inspect = subparsers.add_parser("inspect", help=msg("cli.help.insp"))
    inspect.add_argument("-p", "--project", required=True, help=msg("cli.help.insp.project"))
    inspect.add_argument("-c", "--config", required=False, help=msg("cli.help.insp.config"))
    inspect.add_argument("-s", "--seed", required=False, help=msg("cli.help.insp.seed"))
    inspect.add_argument("-t", "--table", required=False, help=msg("cli.help.insp.table"))
    inspect.add_argument("-r", "--rows", required=False, help=msg("cli.help.insp.rows"))
    inspect.add_argument("-o", "--output-file", required=False, help=msg("cli.help.insp.out"))
    inspect.add_argument("-m", "--schema", required=False, help=msg("cli.help.insp.schema"))
    inspect.add_argument(
        "--insert-batch-size",
        required=False,
        default=1,
        type=int,
        help="Rows per INSERT statement (1 = one INSERT per row).",
    )
