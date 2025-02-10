"""A class to represent an entity in the dataset"""

from dataclasses import dataclass
from typing import Any, cast

from intently_nlu.constants import (
    AUTOMATICALLY_EXTENSIBLE_ENTITY,
    MAP_SYNONYMS_ENTITY,
    MATCHING_STRICTNESS_ENTITY,
    NAME_ENTITY,
    VALUES_ENTITY,
)


@dataclass(frozen=True)
class Entity:
    """Represents a slot entity with all its parameters and values

    This class can represent both custom and builtin entities.

    Args:
        name (str): Name of the entity.
        values (dict[str, str]): Possible or example values for this entity.
                                 If `map_synonyms` is true, the value is used for output instead of the key.
        automatically_extensible (bool, optional): Whether or not the entity can be extended with values
                                                   not present in the data. Defaults to False.
        map_synonyms (bool, optional): Wether or not the first value of synonyms (value in the `values` dictionary)
                                       must be used for output.
                                       This is only guaranteed if `automatically_extensible` is set to `False`,
                                       otherwise some other values which are not in `values` could be parsed.
                                       Defaults to False.
        matching_strictness (float, optional): Controls how similar a value must be to the values used for training.
                                               Defaults to 0.0.
    """

    name: str
    values: dict[str, str]
    automatically_extensible: bool = False
    map_synonyms: bool = False
    matching_strictness: float = 0.0

    @property
    def is_builtin(self) -> bool:
        """Checks if this entity is builtin or custom

        Returns:
            bool: True if it is builtin, False otherwise.
        """
        # pylint: disable=import-outside-toplevel
        from intently_nlu.util.resources import is_builtin_entity

        return is_builtin_entity(self.name)

    @property
    def as_map(self) -> dict[str, Any]:
        """Groups all important data in a JSON serializable dictionary

        Returns:
            dict[str, Any]: JSON serializable dictionary with all important data.
        """
        data_dict: dict[str, Any] = {}
        data_dict[NAME_ENTITY] = self.name
        data_dict[AUTOMATICALLY_EXTENSIBLE_ENTITY] = self.automatically_extensible
        data_dict[MAP_SYNONYMS_ENTITY] = self.map_synonyms
        data_dict[MATCHING_STRICTNESS_ENTITY] = self.matching_strictness
        data_dict[VALUES_ENTITY] = self.values
        return data_dict

    @classmethod
    def from_yaml(cls, yaml_data: dict[str, Any]) -> "Entity":
        """Creates an `Entity` from its YAML definition object

        Args:
            yaml_data (dict[str, Any]): Loaded YAML data.

        Returns:
            Entity: The created Entity.

        Example:
            YAML:
            ```
                type: entity
                name: smarthome/entities/room
                automatically_extensible: no
                values:
                - bedroom
                - [living room, main room, lounge]
                - [garden, yard, backyard]
            ```
        """
        name = yaml_data[NAME_ENTITY]
        values: dict[str, str] = {}

        automatically_extensible = False
        map_synonyms = False
        matching_strictness: float = 0

        if AUTOMATICALLY_EXTENSIBLE_ENTITY in yaml_data:
            automatically_extensible = (
                True if yaml_data[AUTOMATICALLY_EXTENSIBLE_ENTITY] is True else False
            )
        if MAP_SYNONYMS_ENTITY in yaml_data:
            map_synonyms = True if yaml_data[MAP_SYNONYMS_ENTITY] is True else False
        if MATCHING_STRICTNESS_ENTITY in yaml_data:
            matching_strictness = float(yaml_data[MATCHING_STRICTNESS_ENTITY])

        for value in yaml_data[VALUES_ENTITY]:
            if isinstance(value, str):
                values[value] = value
            elif isinstance(value, list):
                value = cast(list[Any], value)
                if all(isinstance(subvalue, str) for subvalue in value):
                    value = cast(list[str], value)
                    for subvalue in value:
                        values[subvalue] = value[0]
        return Entity(
            name, values, automatically_extensible, map_synonyms, matching_strictness
        )
