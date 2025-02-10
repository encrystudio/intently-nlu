"""Utils for representing data"""

import json
from typing import Any


def json_string(json_object: Any, indent: int = 2, sort_keys: bool = True) -> str:
    """Simplified json.dumps(). Serializes `json_object` to a JSON formatted string.

    Args:
        json_object (Any): Object that is JSON-serializable.
        indent (int, optional): JSON indent. Defaults to 2.
        sort_keys (bool, optional): If True, the output of dictionaries will be sorted by key. Defaults to True.

    Returns:
        str: JSON-formatted string.
    """
    return json.dumps(
        json_object, indent=indent, sort_keys=sort_keys, separators=(",", ": ")
    )
