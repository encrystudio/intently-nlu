"""Versions CLI"""


def add_version_parser(subparsers, formatter_class) -> None:  # type: ignore
    """Add the `version` subcommand"""
    # pylint: disable=import-outside-toplevel
    from intently_nlu.__about__ import __version__

    subparser = subparsers.add_parser(  # type: ignore
        "version", formatter_class=formatter_class, help="Print the package version"
    )
    subparser.set_defaults(func=lambda _: print(__version__))  # type: ignore


def add_model_version_parser(subparsers, formatter_class) -> None:  # type: ignore
    """Add the `model-version` subcommand"""
    # pylint: disable=import-outside-toplevel
    from intently_nlu.__about__ import __model_version__

    subparser = subparsers.add_parser(  # type: ignore
        "model-version", formatter_class=formatter_class, help="Print the model version"
    )
    subparser.set_defaults(func=lambda _: print(__model_version__))  # type: ignore
