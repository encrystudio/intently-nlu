# type: ignore
import json

from intently_nlu.dataset.dataset import Dataset
from intently_nlu.dataset.entity import Entity
from intently_nlu.dataset.intent import Intent

ENTITIES = {
    "smarthome/entities/room": {
        "automatically_extensible": False,
        "map_synonyms": False,
        "matching_strictness": 0,
        "name": "smarthome/entities/room",
        "values": {
            "backyard": "garden",
            "bedroom": "bedroom",
            "garden": "garden",
            "living room": "living room",
            "lounge": "living room",
            "main room": "living room",
            "yard": "garden",
        },
    },
    "smarthome/entities/temperature": {
        "automatically_extensible": True,
        "map_synonyms": True,
        "matching_strictness": 0,
        "name": "smarthome/entities/temperature",
        "values": {
            "100 degrees": "100 degrees",
            "20 degrees": "20 degrees",
            "normal": "20 degrees",
            "warm": "20 degrees",
        },
    },
}

INTENTS = {
    "smarthome/intents/setTemperature": {
        "matching_strictness": 0,
        "required_slots": {
            "room": "smarthome/entities/room",
            "room_temperature": "smarthome/entities/temperature",
        },
        "utterances": [
            "Set the temperature to [room_temperature] in the [room]",
            "please set the [room]'s temperature to [room_temperature]",
            "I want [room_temperature] in the [room] please",
            "Can you increase the temperature to [room_temperature]?",
        ],
    },
    "smarthome/intents/turnLightOff": {
        "matching_strictness": 0,
        "required_slots": {"room": "smarthome/entities/room"},
        "utterances": [
            "Turn off the lights in the [room]",
            "turn the [room]'s light out please",
            "switch off the light the [room], will you?",
            "Switch the [room]'s lights off please",
        ],
    },
    "smarthome/intents/turnLightOn": {
        "matching_strictness": 0,
        "required_slots": {"room": "smarthome/entities/room"},
        "utterances": [
            "Turn on the lights in the [room]",
            "give me some light in the [room] please",
            "Can you light up the [room]?",
            "switch the [room]'s lights on please",
        ],
    },
}


def test_dataset():
    d = Dataset.from_yaml("en", ["tests/test_dataset.yaml", "tests/test_dataset2.yaml"])
    assert isinstance(d, Dataset)
    assert d.language == "en"
    for entity_id, entity in d.custom_entities.items():
        assert entity_id in ENTITIES
        assert (
            entity.automatically_extensible
            == ENTITIES[entity_id]["automatically_extensible"]
        )
        assert entity.map_synonyms == ENTITIES[entity_id]["map_synonyms"]
        assert entity.matching_strictness == ENTITIES[entity_id]["matching_strictness"]
        assert entity.name == ENTITIES[entity_id]["name"]
        for value, synonym in entity.values.items():
            assert value in ENTITIES[entity_id]["values"]
            assert synonym == ENTITIES[entity_id]["values"][value]
    for intent_id, intent in d.intents.items():
        assert intent_id in INTENTS
        intent.required_slots == INTENTS[intent_id]["required_slots"]
        intent.utterances == INTENTS[intent_id]["utterances"]

    d = None
    with open("tests/test_dataset.json") as f:
        d = Dataset.from_json(json.load(f))
    assert isinstance(d, Dataset)
    assert d.language == "en"
    for entity_id, entity in d.custom_entities.items():
        assert entity_id in ENTITIES
        assert (
            entity.automatically_extensible
            == ENTITIES[entity_id]["automatically_extensible"]
        )
        assert entity.map_synonyms == ENTITIES[entity_id]["map_synonyms"]
        assert entity.matching_strictness == ENTITIES[entity_id]["matching_strictness"]
        assert entity.name == ENTITIES[entity_id]["name"]
        for value, synonym in entity.values.items():
            assert value in ENTITIES[entity_id]["values"]
            assert synonym == ENTITIES[entity_id]["values"][value]
    for intent_id, intent in d.intents.items():
        assert intent_id in INTENTS
        intent.required_slots == INTENTS[intent_id]["required_slots"]
        intent.utterances == INTENTS[intent_id]["utterances"]
