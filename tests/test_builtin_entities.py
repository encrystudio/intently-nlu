import json
from types import NoneType

from intently_nlu import Dataset, IntentlyNLUEngine

UTTERANCES = {
    "Set the temperature to 100 in the bedroom": "100",
    "please set the bedroom's temperature to -100": "-100",
    "I want 145.57 in the bedroom please": "145.57",
    "Can you decrease the temperature to -54.5?": "-54.5",
}


def test_engine():
    engine = IntentlyNLUEngine()
    d = None
    with open("tests/test_dataset_with_number.json") as f:
        d = Dataset.from_json(json.load(f))
    engine.fit(d)

    assert engine.fitted

    for utterance, slot in UTTERANCES.items():
        result = engine.parse_utterance(utterance)
        assert not isinstance(result, NoneType)
        assert result.resolved_slots["room_temperature"] == slot
