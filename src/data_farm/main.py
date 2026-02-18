import sys

from data_farm.cli.base import build_parser
from data_farm.cli.cli_dispatch import dispatch


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    dispatch(args)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except FileNotFoundError as err:
        print(f"Error: {err}", file=sys.stderr)
        raise SystemExit(1) from err
    except Exception as err:
        import traceback

        traceback.print_exc()
        print(f"Unexpected error: {err}", file=sys.stderr)
        raise SystemExit(1) from err
