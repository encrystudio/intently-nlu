"""A class to represent an intent in the dataset"""

from dataclasses import dataclass
from typing import Any

from intently_nlu.constants import (
    MATCHING_STRICTNESS_INTENT,
    NAME_INTENT,
    OPTIONAL_SLOTS_INTENT,
    REQUIRED_SLOTS_INTENT,
    SLOT_ENTITY,
    SLOT_NAME,
    UTTERANCES_INTENT,
)
from intently_nlu.dataset.entity import Entity


@dataclass(frozen=True)
class Intent:
    """Represents one intent with all its slots and utterances

    Args:
        name (str): Name of the intent.
        utterances (list[str]): A list of example utterances.
        required_slots (dict[str, Entity]): All slots that must be filled, otherwise the intent cannot be parsed.
        optional_slots (dict[str, Entity], optional): All slots that must not necessarily be filled.
                                                      Parsing will not fail if the slot can not be filled,
                                                      but the result will not contain a value for it in that case.
        matching_strictness (float, optional): Controls how similar an utterance must be to the training data.
                                               Defaults to 0.0.
    """

    name: str
    utterances: list[str]
    required_slots: dict[str, Entity]
    optional_slots: dict[str, Entity] | None
    matching_strictness: float = 0.0

    @property
    def all_slots(self) -> dict[str, Entity]:
        """Return all slots of the intent in one single dictionary

        Returns:
            dict[str, Entity]: Required slots + optional slots.
        """
        all_slots: dict[str, Entity] = self.required_slots
        if self.optional_slots is not None:
            all_slots = self.optional_slots | all_slots

        return all_slots

    @property
    def as_map(self) -> dict[str, Any]:
        """Groups all important data in a JSON serializable dictionary

        Returns:
            dict[str, Any]: JSON serializable dictionary with all important data.
        """
        data_dict: dict[Any, Any] = {}
        data_dict[REQUIRED_SLOTS_INTENT] = {
            k: v.name for k, v in self.required_slots.items()
        }
        if self.optional_slots is not None:
            data_dict[OPTIONAL_SLOTS_INTENT] = {
                k: v.name for k, v in self.optional_slots.items()
            }
        data_dict[UTTERANCES_INTENT] = self.utterances
        data_dict[MATCHING_STRICTNESS_INTENT] = self.matching_strictness
        return data_dict

    @classmethod
    def from_yaml(
        cls, yaml_data: dict[str, Any], custom_entities: dict[str, Entity]
    ) -> "Intent":
        """Creates an `Intent` from its YAML definition object

        Args:
            yaml_data (dict[str, Any]): Dictionary containing the YAML definition of the intent.
            custom_entities (dict[str, Entity]): Custom entities that might be used in this intent.

        Returns:
            Intent: The created Intent.

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
            ```
        """
        from intently_nlu.util.resources import (  # pylint: disable=C0415
            get_builtin_entity,
            is_builtin_entity,
        )

        name = yaml_data[NAME_INTENT]
        matching_strictness: float = 0
        utterances: list[str] = []
        required_slots: dict[str, Entity] = {}
        optional_slots: dict[str, Entity] = {}
        if MATCHING_STRICTNESS_INTENT in yaml_data:
            matching_strictness = float(yaml_data[MATCHING_STRICTNESS_INTENT])

        if REQUIRED_SLOTS_INTENT in yaml_data:
            for slot in yaml_data[REQUIRED_SLOTS_INTENT]:
                if is_builtin_entity(slot[SLOT_ENTITY]):
                    required_slots[slot[SLOT_NAME]] = get_builtin_entity(
                        slot[SLOT_ENTITY]
                    )
                else:
                    required_slots[slot[SLOT_NAME]] = custom_entities[slot[SLOT_ENTITY]]
        if OPTIONAL_SLOTS_INTENT in yaml_data:
            for slot in yaml_data[OPTIONAL_SLOTS_INTENT]:
                if is_builtin_entity(slot[SLOT_ENTITY]):
                    optional_slots[slot[SLOT_NAME]] = get_builtin_entity(
                        slot[SLOT_ENTITY]
                    )
                else:
                    optional_slots[slot[SLOT_NAME]] = custom_entities[slot[SLOT_ENTITY]]

        for utterance in yaml_data[UTTERANCES_INTENT]:
            utterances.append(utterance)
        return Intent(
            name,
            utterances,
            required_slots,
            optional_slots if optional_slots else None,
            matching_strictness=matching_strictness,
        )
