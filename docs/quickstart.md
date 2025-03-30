# Quickstart

In this section, we assume that you have installed `intently-nlu` and loaded resources for English:

```bash
python -m pip install intently-nlu
python -m intently_nlu download en
```

The Intently NLU engine needs to be trained on some data before it can start extracting information. Thus, the first thing to do is to build a dataset that can be fed into Intently NLU. For now, we will use this [sample dataset](https://github.com/encrystudio/intently-nlu/tree/main/examples/example.json) which contains data for three intents:

- `setTemperature` -> `"Set the temperature to 20 degrees in the living room"`
- `turnLightOff` -> `"Turn on the light in the kitchen"`
- `turnLightOn` -> `"Turn off the light in the kitchen"`

The format used here is JSON, so let’s load it into a python dict:

```python
import json

with open("path/to/example.json") as f:
    sample_dataset = json.load(f)
```

Now that we have our dataset, we can move forward to the next step which is building an IntentlyNLUEngine. This is the main object of this lib.

```python
from intently_nlu import Dataset, IntentlyNLUEngine

nlu_engine = IntentlyNLUEngine()
```

Now that we have our engine object created, we need to feed it with our sample dataset. In general, this action will require some _machine learning_, so we will actually _fit_ the engine:

```python
nlu_engine.fit(Dataset.from_json(sample_dataset))
```

Our NLU engine is now trained to recognize new utterances that extend beyond what is strictly contained in the dataset: it is able to _generalize_.

Let’s try to parse something now!

```python
parsing = nlu_engine.parse_utterance("Set the temperature to 20 degrees in the bedroom!")
print(parsing.as_json())
```

You should get something that looks like this:

```json
{
  "intent": "smarthome/intents/setTemperature",
  "probability": 1.0,
  "raw_utterance": "Set the temperature to 20 degrees in the bedroom!",
  "resolved_slots": {
    "room": "bedroom",
    "room_temperature": "20 degrees"
  }
}
```

Congrats, you parsed your first intent!
