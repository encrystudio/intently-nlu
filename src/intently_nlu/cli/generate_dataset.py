"""Dataset generation CLI"""


def add_generate_dataset_subparser(subparsers, formatter_class) -> None:  # type: ignore
    """Add the `generate-dataset` subcommand"""
    subparser = subparsers.add_parser(  # type: ignore
        "generate-dataset",
        formatter_class=formatter_class,
        help="Generate a JSON dataset from intents and entities YAML file(s)",
    )
    subparser.add_argument("language", type=str, help="Language of the dataset")  # type: ignore
    subparser.add_argument("files", nargs="+", type=str, help="Intent and entity YAML file(s)")  # type: ignore
    subparser.set_defaults(func=_generate_dataset)  # type: ignore


def _generate_dataset(args_namespace) -> None:  # type: ignore
    generate_dataset(args_namespace.language, args_namespace.files)  # type: ignore


def generate_dataset(language: str, yaml_files: list[str]) -> None:
    """Creates an IntentlyNLU dataset from YAML definition file(s)

    Args:
        language (str): Language of the dataset (ISO639-1 language code).
        yaml_files (list[str]): Path to intent and entity definition file(s) in YAML format.

    Returns:
        None: The json dataset output is printed out on stdout.
    """
    # pylint: disable=import-outside-toplevel
    from intently_nlu.dataset.dataset import Dataset
    from intently_nlu.util.intently_logging import get_logger
    from intently_nlu.util.representation import json_string

    logger = get_logger(__name__)

    logger.info("Generate Dataset from YAML...")
    dataset = Dataset.from_yaml(language, yaml_files)
    logger.info("Generate Dataset from YAML...Done!")
    print(json_string(dataset.as_json))
