"""A class to represent all the data in a JSON dataset"""

from dataclasses import dataclass, field
from typing import Any

import yaml

from intently_nlu.constants import (
    AUTOMATICALLY_EXTENSIBLE_ENTITY,
    ENTITIES_JSON,
    ENTITY_YAML,
    INTENT_YAML,
    INTENTS_JSON,
    LANGUAGE_JSON,
    MAP_SYNONYMS_ENTITY,
    MATCHING_STRICTNESS_ENTITY,
    MATCHING_STRICTNESS_INTENT,
    NAME_ENTITY,
    OPTIONAL_SLOTS_INTENT,
    REQUIRED_SLOTS_INTENT,
    TYPE_YAML,
    UTTERANCES_INTENT,
    VALUES_ENTITY,
)
from intently_nlu.dataset.entity import Entity
from intently_nlu.dataset.intent import Intent


@dataclass(frozen=True)
class Dataset:
    """A `Dataset` is used for training the NLU components

    Consists of `Intent` and `Entity` data.
    This object can be built either from JSON files (`Dataset.from_json()`)
    or from YAML files (`Dataset.from_yaml()`).

    Args:
        language (str): ISO639-1 Language code of the dataset.
        intents (dict[str, Intent]): All intents the dataset contains.
        custom_entities (dict[str, Entity], optional): Custom entities used in the intents, if any.
                                                       Defaults to an empty list.
    """

    language: str
    intents: dict[str, Intent]
    custom_entities: dict[str, Entity] = field(default_factory=dict[str, Entity])

    @property
    def is_valid(self) -> bool:
        """Checks if the dataset is valid in terms of logic and compatibility

        Returns:
            bool: True if dataset is valid.
        """
        from intently_nlu.util.language import (  # pylint: disable=C0415
            is_valid_supported_language_code,
        )

        valid_intents = True
        for intent in self.intents.values():
            valid_intents = valid_intents and len(intent.utterances) > 0

        return (
            is_valid_supported_language_code(self.language)
            and len(self.intents) > 0
            and valid_intents
        )

    @property
    def as_json(self) -> dict[str, Any]:
        """Groups all data in a compact, json serializable format

        Returns:
            dict[str, Any]: All important data in one dictionary.
        """
        json_dict: dict[str, Any] = {}
        json_dict[LANGUAGE_JSON] = self.language
        intents: dict[str, dict[Any, Any]] = {}
        for intent in self.intents:
            intents[intent] = self.intents[intent].as_map
        json_dict[INTENTS_JSON] = intents
        entities: dict[str, dict[Any, Any]] = {}
        for entity_id, entity in self.custom_entities.items():
            entities[entity_id] = entity.as_map
        json_dict[ENTITIES_JSON] = entities
        return json_dict

    @classmethod
    def from_json(cls, json: dict[str, Any]) -> "Dataset":
        """Creates a `Dataset` from a JSON dict

        Args:
            json (dict[str, Any]): Parsed JSON file

        Returns:
            Dataset: Generated `Dataset`.
        Example:
            JSON:
            ```
                {
                  "entities": {
                    "smarthome/entities/room": {
                      "automatically_extensible": false,
                      "map_synonyms": false,
                      "matching_strictness": 0,
                      "name": "smarthome/entities/room",
                      "values": {
                        "backyard": "garden",
                        "bedroom": "bedroom",
                        "garden": "garden",
                        "living room": "living room",
                        "lounge": "living room",
                        "main room": "living room",
                        "yard": "garden"
                      }
                    }
                  },
                  "intents": {
                    "smarthome/intents/turnLightOn": {
                      "matching_strictness": 0,
                      "required_slots": {
                        "room": "smarthome/entities/room"
                      },
                      "utterances": [
                        "Turn on the lights in the [room]",
                        "give me some light in the [room] please",
                        "Can you light up the [room]?",
                        "switch the [room]'s lights on please"
                      ]
                    }
                  },
                  "language": "en"
                }
            ```
        """
        from intently_nlu.util.resources import (  # pylint: disable=C0415
            get_builtin_entity,
            is_builtin_entity,
        )

        intents: dict[str, Intent] = {}
        custom_entities: dict[str, Entity] = {}

        if ENTITIES_JSON in json:
            for entity in json[ENTITIES_JSON].values():
                entity = Entity(
                    entity[NAME_ENTITY],
                    entity[VALUES_ENTITY],
                    entity[AUTOMATICALLY_EXTENSIBLE_ENTITY],
                    entity[MAP_SYNONYMS_ENTITY],
                    entity[MATCHING_STRICTNESS_ENTITY],
                )
                custom_entities[entity.name] = entity

        for intent in json[INTENTS_JSON].items():
            required_slots: dict[str, Entity] = {}
            optional_slots: dict[str, Entity] = {}
            if REQUIRED_SLOTS_INTENT in intent[1]:
                for slot in intent[1][REQUIRED_SLOTS_INTENT].items():
                    if is_builtin_entity(slot[1]):
                        required_slots[slot[0]] = get_builtin_entity(slot[1])
                    else:
                        required_slots[slot[0]] = custom_entities[slot[1]]
            if OPTIONAL_SLOTS_INTENT in intent[1]:
                for slot in intent[1][OPTIONAL_SLOTS_INTENT].items():
                    if is_builtin_entity(slot[1]):
                        optional_slots[slot[0]] = get_builtin_entity(slot[1])
                    else:
                        optional_slots[slot[0]] = custom_entities[slot[1]]

            intents[intent[0]] = Intent(
                intent[0],
                intent[1][UTTERANCES_INTENT],
                required_slots,
                optional_slots,
                matching_strictness=intent[1][MATCHING_STRICTNESS_INTENT],
            )

        return Dataset(json[LANGUAGE_JSON], intents, custom_entities)

    @classmethod
    def from_yaml(cls, language: str, yaml_files: list[str]) -> "Dataset":
        """Creates `Dataset` from a language and a list of loaded YAML files

        Each file must not correspond to a single entity or intent. They can
        consist of several entities and intents merged together in a single
        file.

        Args:
            language (str): ISO639-1 Language of the dataset.
            yaml_files (list[str]): List of loaded yaml files.

        Returns:
            Dataset: Generated Dataset.

        Example:
            YAML:
            ```
                type: intent
                name: smarthome/intents/turnLightOn
                required_slots:
                  - name: room
                    entity: smarthome/entities/room
                utterances:
                  - Turn on the lights in the [room]
                  - give me some light in the [room] please
                  - Can you light up the [room]?
                  - switch the [room]'s lights on please

                ---
                type: entity
                name: smarthome/entities/room
                automatically_extensible: no
                values:
                - bedroom
                - [living room, main room, lounge]
                - [garden, yard, backyard]
            ```
        """
        intents: dict[str, Intent] = {}
        custom_entities: dict[str, Entity] = {}
        loaded_yaml: list[Any] = []
        for file_path in yaml_files:
            with open(file_path, "r", encoding="utf-8") as file:
                loaded_yaml += yaml.safe_load_all(file)
        for yaml_data in loaded_yaml:
            if yaml_data[TYPE_YAML] == ENTITY_YAML:
                entity = Entity.from_yaml(yaml_data)
                custom_entities[entity.name] = entity
        for yaml_data in loaded_yaml:
            if yaml_data[TYPE_YAML] == INTENT_YAML:
                intent = Intent.from_yaml(yaml_data, custom_entities)
                intents[intent.name] = intent
        return Dataset(language, intents, custom_entities)

    def __str__(self) -> str:
        return str(self.as_json)
