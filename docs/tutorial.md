# Tutorial

In this section, we will build an NLU assistant for home automation tasks. It will be able to understand queries about lights and thermostats. More precisely, our assistant will contain three [intents](data_model.md#intent):

- `turnLightOn`
- `turnLightOff`
- `setTemperature`

The first two intents will be about turning on and off the lights in a specific room. These intents will have one [Slot](data_model.md#slot) which will be the `room`. The third intent will let you control the temperature of a specific room. It will have two slots: the `roomTemperature` and the `room`.

The first step is to create an appropriate dataset for this task.

## Table of contents

- [Tutorial](#tutorial)
  - [Table of contents](#table-of-contents)
  - [Training data](#training-data)
  - [The Intently NLU Engine](#the-intently-nlu-engine)
  - [Training the Engine](#training-the-engine)
  - [Parsing](#parsing)
  - [`None`](#none)
  - [Persisting](#persisting)

## Training data

Check the [Training Dataset Format](dataset.md) section for more details about the format used to describe the training data.

In this tutorial, we will create a `dataset.yaml` file with the following content:

```yaml
# turnLightOn intent
---
type: intent
name: turnLightOn
required_slots:
  - name: room
    entity: entities/room
utterances:
  - Turn on the lights in the [room]
  - give me some light in the [room] please
  - Can you light up the [room]?
  - switch the [room]'s lights on please

# turnLightOff intent
---
type: intent
name: turnLightOff
required_slots:
  - name: room
    entity: entities/room
utterances:
  - Turn off the lights in the [room]
  - turn the [room]'s light out please
  - switch off the light the [room], will you?
  - Switch the [room]'s lights off please

# setTemperature intent
---
type: intent
name: setTemperature
required_slots:
  - name: room_temperature
    entity: entities/temperature
optional_slots:
  - name: room
    entity: entities/room
utterances:
  - Set the temperature to [room_temperature] in the [room]
  - please set the [room]'s temperature to [room_temperature]
  - I want [room_temperature] in the [room] please
  - Can you increase the temperature to [room_temperature]?

# room entity
---
type: entity
name: entities/room
values:
  - bedroom
  - [living room, main room, lounge]
  - [garden, yard, backyard]

# room temperature entity
---
type: entity
name: entities/temperature
automatically_extensible: no
map_synonyms: yes
values:
  - 100 degrees
  - [20 degrees, warm, normal]
```

Here, we put all the intents and entities in the same file but we could have split them in dedicated files as well.

The `entities/temperature` entity has a `map_synonyms: yes`, so it will map the [synonyms](data_model.md#entity-values--synonyms) (20 degrees, warm, normal) to the first item of the list (20 degrees). Note that `entities/room` has lists as values too, but no `map_synonyms: yes` so it won't map [synonyms](data_model.md#entity-values--synonyms). You can read more about the defaults here.

Besides, both entities are marked as not [automatically extensible](data_model.md#automatically-extensible-entities) which means that the NLU will only output values that we have defined and will not try to match other values.

We are now ready to generate our dataset using the [CLI](cli.md):

```bash
python -m intently_nlu generate_dataset en dataset.yaml
```

Now that we have our dataset ready, let’s move to the next step which is to create an NLU engine.

## The Intently NLU Engine

The main API of Intently NLU is an object called `IntentlyNLUEngine`. This engine is the one you will train and use for parsing.

The simplest way to create an NLU engine is the following:

```python
from intently_nlu import IntentlyNLUEngine

engine = IntentlyNLUEngine()
```

In this example the engine was created with default parameters which, in many cases, will be sufficient.

<!-- However, in some cases it may be required to tune the engine a bit and provide a customized configuration. You can check the [IntentlyNLUEngineConfig](configuration.md) to get more details about what can be configured. -->

At this point, we can try to parse something:

```python
engine.parse_utterance("Please give me some lights in the bedroom!")
```

That will raise a `NotTrained` error, as we did not train the engine with the dataset that we created.

## Training the Engine

In order to use the engine we created, we need to _train_ it or _fit_ it with the dataset we generated earlier:

```python
from intently_nlu import Dataset
import json

with open("dataset.json") as f:
    dataset = Dataset.from_json(json.load(f))

engine.fit(dataset)
```

## Parsing

We are now ready to parse:

```python
result = engine.parse_utterance("Turn on the lights in the bedroom!")
print(result.as_json())
```

You should get the following output or similar:

```json
{
  "intent": "smarthome/intents/turnLightOn",
  "probability": 1.0,
  "raw_utterance": "Turn on the lights in the bedroom!",
  "resolved_slots": {
    "room": "bedroom"
  }
}
```

## `None`

If none of the intents that you have declared in your dataset can be classified for the utterance or if some required slots are missing, the NLU engine returns `None`.

## Persisting

As a final step, we will persist the engine into a file. That may be useful in various contexts, for instance if you want to train on a machine and parse on another one. The file extension of an IntentlyNLUEngine is `.inlue`.

You can persist the engine with the following API:

```python
engine.persist("path/to/file")
```

And load it:

```python
loaded_engine = IntentlyNLUEngine.from_file("path/to/file")
loaded_engine.parse_utterance("Turn on the lights in the bedroom!")
```
