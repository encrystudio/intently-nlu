"""Inference CLI"""


def add_parse_parser(subparsers, formatter_class) -> None:  # type: ignore
    """Add the `parse` subcommand"""
    subparser = subparsers.add_parser(  # type: ignore
        "parse",
        formatter_class=formatter_class,
        help="Load a trained IntentlyNLU engine and perform parsing",
    )
    subparser.add_argument(  # type: ignore
        "engine", type=str, help="Path to a trained engine file"
    )
    subparser.add_argument(  # type: ignore
        "-q",
        "--query",
        type=str,
        help="Query to parse. If provided, it disables the interactive behavior.",
    )
    subparser.set_defaults(func=_parse)  # type: ignore


def _parse(args_namespace) -> None:  # type: ignore
    parse(args_namespace.engine, args_namespace.query)  # type: ignore


def parse(engine: str, query: str | None) -> None:
    """Load a trained IntentlyNLU engine and play with its parsing API interactively.

    Args:
        engine (str): Path to a trained engine file.
        query (str, optional): Query to parse. If provided, it disables the interactive behavior.
    """
    # pylint: disable=import-outside-toplevel
    from intently_nlu import IntentlyNLUEngine
    from intently_nlu.nlu_engine import IntentlyNLUResult
    from intently_nlu.util.intently_logging import get_logger
    from intently_nlu.util.representation import json_string

    logger = get_logger(__name__)
    logger.info("Parse command startet!")
    logger.debug("  Load engine from file...")
    engine: IntentlyNLUEngine = IntentlyNLUEngine.from_file(engine)
    logger.debug("  Load engine from file...Done!")

    if query is not None:
        logger.debug("  Perform parsing...")
        result: IntentlyNLUResult | None = engine.parse_utterance(query)
        if result is None:
            print("None")
            logger.info("       RESULT: None")
        else:
            print(json_string(result.__dict__))
            logger.info("       RESULT: %s", json_string(result.__dict__))
        logger.debug("  Perform parsing...Done!")
        logger.info("Parse command finished!")
        return

    while True:
        query = input("Enter a query (type 'q' to quit): ").strip()
        logger.debug("   Query: %s", query)
        if query == "q":
            logger.debug("  'q' recognized, quitting!")
            break
        logger.debug("  Perform parsing...")
        result: IntentlyNLUResult | None = engine.parse_utterance(query)
        if result is None:
            print("None")
            logger.info("       RESULT: None")
        else:
            print(json_string(result.__dict__))
            logger.info("       RESULT: %s", json_string(result.__dict__))
        logger.debug("  Perform parsing...Done!")
    logger.info("Parse command finished!")
