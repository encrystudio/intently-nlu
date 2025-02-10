"""Utils for string normalization"""

import re

from intently_nlu.util.language import get_punctuation


def normalize(
    string: str,
    to_lower_case: bool = False,
    strip_whitespace: bool = True,
    try_remove_punctuation: bool = False,
    lang: str = "",
) -> str:
    """String normalization

    Args:
        text (str): The text to normalize.
        to_lower_case (bool, optional): Convert every character to lower case. Defaults to False.
        strip_whitespace (bool, optional): Remove leading and trailing whitespace. Defaults to True.
        remove_punctuation (bool, optional): Remove punctuation of the text. Requires `lang`. Defaults to False.
        lang (str, optional): Language of the text. Only necessary for some normalization actions.

    Returns:
        str: Normalized String.
    """
    string = string.lower() if to_lower_case else string
    string = string.strip() if strip_whitespace else string
    string = remove_punctuation(string, lang) if try_remove_punctuation else string
    string = string.strip() if strip_whitespace else string
    return string


def remove_punctuation(text: str, lang: str) -> str:
    """Removes punctuation of the text for a specific language

    The data is provided by the language data.
    Decimal separators will be ignored.

    Args:
        text (str): The text from which punctuation will be removed.
        lang (str): Language code of the text.

    Returns:
        str: `text` with punctuation removed.

    Example:
        >>> from intently_nlu.utils.normalization import remove_punctuation
        >>> print(remove_punctuation("This is an example. It contains a number: 1.0!", "en"))
        This is an example It contains a number 1.0
    """
    lang_punct = "".join(get_punctuation(lang))
    regex = re.compile(
        rf"(?<![0-9])[{lang_punct}](?![0-9])|(?<=[0-9])[{lang_punct}](?![0-9])|(?<![0-9])[{lang_punct}](?=[0-9])"
    )
    text = re.sub(regex, "", text)

    return text
