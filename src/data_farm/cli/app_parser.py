from __future__ import annotations

from argparse import ArgumentParser

from data_farm.messages.messages import msg


def build_app_parser(parser: ArgumentParser) -> None:
    parser.add_argument("-v", "--verbose", action="count", default=0, help=msg("cli.help.global.verbose"))
    parser.add_argument("-l", "--log-file", type=str, help=msg("cli.help.global.log_file"))
    parser.add_argument("-d", "--debug", action="store_true", required=False, help=msg("cli.help.global.debug"))
    parser.add_argument("-c", "--config-dir", default=None, required=False, help=msg("cli.help.app.ovr_cfg_dir"))
    parser.add_argument("-a", "--data-dir", default=None, required=False, help=msg("cli.help.app.ovr_data_dir"))
    parser.add_argument("-p", "--config-path", default=None, required=False, help=msg("cli.help.app.ovr_cfg_path"))
    parser.add_argument("-s", "--seed", default=None, required=False, help=msg("cli.help.rng.seed"))
