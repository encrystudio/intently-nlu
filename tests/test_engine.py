import json
from types import NoneType

from intently_nlu import Dataset, IntentlyNLUEngine

UTTERANCES = {
    "Set the temperature to 100 in the bedroom": "smarthome/intents/setTemperature",
    "please set the bedroom's temperature to 70": "smarthome/intents/setTemperature",
    "I want 70 in the bedroom please": "smarthome/intents/setTemperature",
    "Can you increase the temperature to 70?": "smarthome/intents/setTemperature",
    "Turn on the lights in the bedroom": "smarthome/intents/turnLightOn",
    "give me some light in the bedroom please": "smarthome/intents/turnLightOn",
    "Can you light up the bedroom?": "smarthome/intents/turnLightOn",
    "switch the bedroom's lights on please": "smarthome/intents/turnLightOn",
    "Turn off the lights in the bedroom": "smarthome/intents/turnLightOff",
    "turn the bedroom's light out please": "smarthome/intents/turnLightOff",
    "switch off the light the bedroom, will you?": "smarthome/intents/turnLightOff",
    "Switch the bedroom's lights off please": "smarthome/intents/turnLightOff",
}


def test_engine():
    engine = IntentlyNLUEngine()
    d = None
    with open("tests/test_dataset.json") as f:
        d = Dataset.from_json(json.load(f))
    engine.fit(d)

    assert engine.fitted

    for utterance, intent in UTTERANCES.items():
        result = engine.parse_utterance(utterance)
        assert not isinstance(result, NoneType)
        assert result.intent == intent
