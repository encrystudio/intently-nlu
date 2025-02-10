"""Utils for languages"""

import json
from pathlib import Path

from intently_nlu.constants import OFFICIALLY_SUPPORTED_LANGUAGES, PUNCTUATION
from intently_nlu.exceptions import ResourceError
from intently_nlu.util.intently_logging import get_logger, log_error
from intently_nlu.util.resources import check_for_resource


def is_valid_supported_language_code(lang: str) -> bool:
    """Checks if the language code is valid an supported by the package

    Args:
        lang (str): The language code.

    Returns:
        bool: True if the language code is valid else False.
    """
    if lang in OFFICIALLY_SUPPORTED_LANGUAGES:
        return True
    try:
        check_for_resource(f"languages/{lang}.json")
        return True
    except ResourceError:
        return False


def get_punctuation(lang: str) -> list[str]:
    """Returns the punctuation of a language

    Args:
        lang (str): The language code.

    Returns:
        list[str]: The punctuation of the language.
    """
    path = ""
    try:
        path = check_for_resource(f"languages/{lang}.json")
    except ResourceError as e:
        get_logger(__name__).error(
            "The language resources of %s are not installed. Please install them using 'python -m intently_nlu download %s'",  # pylint: disable=C0301
            lang,
            lang,
        )
        raise log_error(get_logger(__name__), e, f"Get punctuation of '{lang}'") from e
    data = None
    with Path(path).open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data[PUNCTUATION]
