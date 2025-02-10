"""Environment cleanup CLI"""

import os

from intently_nlu.util.intently_logging import get_log_file


def add_cleanup_parser(subparsers, formatter_class) -> None:  # type: ignore
    """Add the `cleanup` subcommand"""
    subparser = subparsers.add_parser(  # type: ignore
        "cleanup",
        formatter_class=formatter_class,
        help="Delete logs and/or remove downloaded resources (TODO)",
    )
    subparser.add_argument("-l", "--log_file", type=bool, help="Delete the logs.", default=True)  # type: ignore
    subparser.add_argument("-r", "--resources", type=bool, help="Delete downloaded resources.", default=True)  # type: ignore # pylint: disable=C0301
    subparser.set_defaults(func=_cleanup)  # type: ignore


def _cleanup(args_namespace) -> None:  # type: ignore
    cleanup(args_namespace.log_file, args_namespace.resources)  # type: ignore


def cleanup(delete_logfile: bool, delete_resources: bool) -> None:
    """Performs system cleanup actions, according to the given args.

    Args:
        delete_logfile (bool): If true, deletes the content of the log file.
    """
    from intently_nlu.util.intently_logging import (  # pylint: disable=import-outside-toplevel
        get_logger,
    )

    logger = get_logger(__name__)

    logger.info("Cleanup...")

    if delete_logfile:
        logger.debug("  Delete logs...")
        with open(
            os.fspath(get_log_file()),
            "r+",
            encoding="utf-8",
        ) as logs:
            logs.truncate(0)
        logger.debug("  Delete logs...Done!")
    if delete_resources:
        logger.debug("  Delete resources...")
        # pylint: disable=import-outside-toplevel
        import shutil

        from platformdirs import user_data_dir

        shutil.rmtree(
            os.path.join(
                user_data_dir(appname="intently-nlu", appauthor="encrystudio"),
                "resources",
            )
        )
        logger.debug("  Delete resources...Done!")
    logger.info("Cleanup...Done!")
