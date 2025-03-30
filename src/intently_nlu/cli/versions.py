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

    subparser = subparsers.add_parser(  # type: ignore
        "model-version",
        formatter_class=formatter_class,
        help="Print the model version of a persisted engine or the current",
    )
    subparser.add_argument(  # type: ignore
        "-p", "--path", type=str, help=" Path to a trained engine file"
    )
    subparser.set_defaults(func=_model_version)  # type: ignore


def _model_version(args_namespace) -> None:  # type: ignore
    model_version(
        args_namespace.path,  # type: ignore
    )


def model_version(path: str | None) -> None:  # type: ignore
    """Print the current model version or, if provided, the model version of a persisted engine

    Args:
        path (str | None): Path to a trained engine file.
    """
    # pylint: disable=import-outside-toplevel
    from intently_nlu.__about__ import __model_version__

    if path is None:
        print(__model_version__)
    else:
        # pylint: disable=import-outside-toplevel
        from intently_nlu import IntentlyNLUEngine

        engine: IntentlyNLUEngine = IntentlyNLUEngine.from_file(path, True)
        print(engine.version)
