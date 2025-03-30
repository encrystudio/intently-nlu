"""Training CLI"""

from intently_nlu.nlu_engine import IntentlyNLUEngineConfig


def add_train_parser(subparsers, formatter_class) -> None:  # type: ignore
    """Add the `train` subcommand"""
    subparser = subparsers.add_parser(  # type: ignore
        "train",
        formatter_class=formatter_class,
        help="Train an IntentlyNLU engine on a provided JSON dataset",
    )
    subparser.add_argument(  # type: ignore
        "dataset_path", type=str, help="Path to the JSON training dataset file"
    )
    subparser.add_argument("engine_out", type=str, help="Path to store the trained engine as a file.")  # type: ignore
    subparser.add_argument(  # type: ignore
        "-c", "--config_path", type=str, help="Path to a NLU engine configuration JSON)"
    )
    subparser.set_defaults(func=_train)  # type: ignore


def _train(args_namespace) -> None:  # type: ignore
    train(
        args_namespace.dataset_path,  # type: ignore
        args_namespace.engine_out,  # type: ignore
        args_namespace.config_path,  # type: ignore
    )


def train(dataset_path: str, engine_out: str, config_path: str | None) -> None:
    """Train an IntentlyNLU engine with the provided JSON dataset

    Args:
        dataset_path (str): Path to the JSON dataset.
        engine_out (str): Path where the engine will be saved to.
        config_path (str, optional): Path to an IntentlyNLU engine configuration JSON,
                                     if provided it will be used to override the default configuration.
    """
    # pylint: disable=import-outside-toplevel
    import json
    from pathlib import Path

    from intently_nlu import IntentlyNLUEngine
    from intently_nlu.dataset.dataset import Dataset
    from intently_nlu.util.intently_logging import get_logger

    logger = get_logger(__name__)
    logger.info("Train command started!")
    logger.debug("  Loading JSON dataset...")
    dataset = None
    with Path(dataset_path).open("r", encoding="utf-8") as f:
        dataset = json.load(f)
    dataset = Dataset.from_json(dataset)
    logger.debug("  Loading JSON dataset...Done!")

    config: None | IntentlyNLUEngineConfig = None
    if config_path is not None:
        logger.debug("  Loading config...")
        with Path(config_path).open("r", encoding="utf-8") as f:
            config = IntentlyNLUEngineConfig.from_json(json.load(f))
        logger.debug("  Loading config...Done!")
    else:
        logger.debug("  No config_path provided. Using default config.")

    logger.info("   Create and train the engine...")
    engine = IntentlyNLUEngine(config).fit(dataset)
    logger.info("   Create and train the engine...Done!")

    logger.info("   Persisting the engine...")
    path = engine.persist(engine_out)
    logger.info("   Persisting the engine...Done!")

    print(path)
    logger.info("   Saved the trained engine to %s", path)
    logger.info("Train command finished!")
