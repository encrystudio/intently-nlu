"""Utils for intently resources."""

import os

from platformdirs import user_data_dir

from intently_nlu.dataset.entity import Entity
from intently_nlu.exceptions import ResourceError


def is_builtin_entity(name: str) -> bool:
    """Checks if the entity is a builtin entity

    Args:
        name (str): Name of the entity.

    Returns:
        bool: True if it is a builtin, else false.
    """
    from intently_nlu.constants import BUILTIN_ENTITY_NAMES  # pylint: disable=C0415

    return name in BUILTIN_ENTITY_NAMES


def get_builtin_entity(name: str) -> Entity:
    """Returns the builtin entity

    Args:
        name (str): Name of the entity.

    Returns:
        Entity: The builtin entity.
    """
    from intently_nlu.builtin_entities import BUILTIN_ENTITIES  # pylint: disable=C0415

    return BUILTIN_ENTITIES[name]()


def check_for_resource(name: str):
    """Checks if the requested resource exists and return the path

    Args:
        name (str): The resource identifier.

    Raises:
        ResourceError: Raised if the resource is not available.

    Returns:
        str: Path to the resource.
    """
    data_dir = user_data_dir(appname="intently-nlu", appauthor="encrystudio")
    name = name.replace("/", os.sep)
    resource = os.path.join(data_dir, "resources", name)
    if os.path.exists(resource):
        return resource
    resource = os.path.join(os.getcwd(), "resources", name)
    if os.path.exists(resource):
        return resource
    raise ResourceError(f"Resource not installed: {name}")
