from __future__ import annotations

import sys

from data_farm.l3_frameworks_and_drivers.cli.base import build_parser
from data_farm.l3_frameworks_and_drivers.cli.cli_dispatch import dispatch


def main(argv: list[str] | None = None) -> int:
    """
    Return a process exit code (0 success, non-zero failure).
    No SystemExit raised here; keep it test-friendly.
    """
    if argv is None:
        argv = sys.argv[1:]

    try:
        parser = build_parser()
        args = parser.parse_args(argv)
        return dispatch(parser, args)

    except FileNotFoundError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1

    except Exception as err:
        print(f"Unexpected error: {err}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
