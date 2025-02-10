"""CLI initialization"""

import argparse
import sys

from intently_nlu.__about__ import __version__
from intently_nlu.util.intently_logging import (
    LogLevel,
    initialize_session,
    log_level_cli_map,
)


class Formatter(argparse.ArgumentDefaultsHelpFormatter):
    """Argument help formatter"""

    def __init__(self, prog: str):
        super().__init__(prog, max_help_position=35, width=150)


def get_arg_parser() -> argparse.ArgumentParser:
    """Initialise the argument parser for the CLI

    Returns:
        argparse.ArgumentParser: Initialized argument parser.
    """
    # pylint: disable=import-outside-toplevel
    from .cleanup import add_cleanup_parser  # type: ignore
    from .download import add_download_parser  # type: ignore
    from .generate_dataset import add_generate_dataset_subparser  # type: ignore
    from .inference import add_parse_parser  # type: ignore
    from .training import add_train_parser  # type: ignore
    from .versions import add_model_version_parser  # type: ignore
    from .versions import add_version_parser  # type: ignore

    arg_parser = argparse.ArgumentParser(
        description=f"IntentlyNLU command line interface, version {__version__}",
        prog="python -m intently_nlu",
        formatter_class=Formatter,
    )
    arg_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output using loglevel 0",
        default=False,
    )
    arg_parser.add_argument(
        "-l",
        "--loglevel",
        type=int,
        choices=range(0, 5),
        metavar="LOGLEVEL",
        help="Set the logging level (0: Debug | 1: Info | 2: Warning | 3: Error | 4: Critical)",
        default=2,
    )
    subparsers = arg_parser.add_subparsers(
        title="available commands", metavar="command [options ...]"
    )
    add_generate_dataset_subparser(subparsers, formatter_class=Formatter)
    add_train_parser(subparsers, formatter_class=Formatter)
    add_parse_parser(subparsers, formatter_class=Formatter)
    add_version_parser(subparsers, formatter_class=Formatter)
    add_model_version_parser(subparsers, formatter_class=Formatter)
    add_cleanup_parser(subparsers, formatter_class=Formatter)
    add_download_parser(subparsers, formatter_class=Formatter)
    return arg_parser


def main() -> None:
    """The main entrypoint to IntentlyNLU CLI

    help: `python -m intently_nlu` or `python -m intently_nlu -h`
    """
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    logging_level = log_level_cli_map.get(
        0 if args.verbose else args.loglevel, LogLevel.INFO
    )
    initialize_session(logging_level)

    if hasattr(args, "func"):
        args.func(args)
    elif hasattr(args, "version") and args.version:
        print(f"IntentlyNLU, version {__version__}")
    else:
        arg_parser.print_help()
        sys.exit(0)
