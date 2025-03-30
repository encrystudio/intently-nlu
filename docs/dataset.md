# Training Dataset Format

The Intently NLU library leverages machine learning algorithms and some training data in order to produce a powerful intent recognition engine.

The better your training data is, the more accurate your NLU engine will be. Thus, it is worth spending a bit of time to create a dataset that matches your use case well.

Intently NLU accepts two different dataset formats. The first one, which relies on YAML, is the preferred option if you want to create or edit a dataset manually. The other dataset format uses JSON and should rather be used if you plan to create or edit datasets programmatically.

## Table of contents

- [Training Dataset Format](#training-dataset-format)
  - [Table of contents](#table-of-contents)
  - [YAML format](#yaml-format)
    - [Entity](#entity)
      - [Entity attributes](#entity-attributes)
    - [Intent](#intent)
      - [Intent attributes](#intent-attributes)
    - [Dataset](#dataset)
  - [JSON format](#json-format)

## YAML format

The YAML dataset format allows you to define intents and entities using the [YAML](https://yaml.org/about.html) syntax.

### Entity

Here is what a minimal entity file looks like:

```yaml
# city entity
---
type: entity
name: city
values:
  - berlin
```

The name of an entity can be anything you want. We recommend using a _namespace_ to avoid name collisions. A _namespace_ is typically something like this: `group/entities/entity_name`. In our example, it could be `flights/entities/city`.

You can specify entity values either using single YAML scalars (e.g. `berlin`), or using lists (e.g. `[berlin, new york, tokyo]`). If you don’t set `map_synonyms` to `true`, every value in a list will be treated as a single value. Otherwise they will be used as [synonyms](data_model.md#entity-values--synonyms).

Here is a more comprehensive example which contains all additional attributes that are optional:

```yaml
# city entity
---
type: entity
name: flights/entities/city
automatically_extensible: true # default value is false
map_synonyms: true # default value is false
matching_strictness: 1.0 # default value is 0.0
values:
  - berlin
  - [new york, big apple]
  - tokyo
```

#### Entity attributes

- `type`: Must be set to `entity`
- `name`: Name(space) of the entity
- `automatically_extensible`: Whether or not the entity can be extended with values not present in the data. Defaults to `false`
- `map_synonyms`: Wether or not the first value of the synonyms list must be used for output. This is only guaranteed if `automatically_extensible` is set to `false`, otherwise some other values which are not in `values` could be parsed. Defaults to `false`
- `matching_strictness`: Controls how similar a value must be to the values used for training. Defaults to `0.0`
- `values`: Possible (if `automatically_extensible` is `false`) or example (if `automatically_extensible` is `true`) values for this entity.

### Intent

Here is the minimal format used to describe an intent:

```yaml
# turnLightOn intent
---
type: intent
name: turnLightOn
utterances:
  - Turn on the lights.
```

The name of an intent can be anything you want. We recommend using a _namespace_ to avoid name collisions. A _namespace_ is typically something like this: `group/intents/intent_name`. In our example, it could be `home_assistant/intents/turnLightOn`.

An intent is not required to have any slots. However, if it does have slots, they must be defined in the `required_slots` or `optional_slots` attributes:

```yaml
# setTemperature intent
---
type: intent
name: home_assistant/intents/setTemperature
required_slots: # Parsing will fail if these slots can not be filled
  - name: room_temperature
    entity: home_assistant/entities/temperature
optional_slots: # If recognized, these slots will be filled, but parsing will not fail if not
  - name: room
    entity: home_assistant/entities/room
matching_strictness: 0.5
utterances:
  - Set the temperature to [room_temperature] in the [room]
  - please set the [room]'s temperature to [room_temperature]
  - I want [room_temperature] in the [room] please
  - Can you increase the temperature to [room_temperature]?
```

#### Intent attributes

- `type`: Must be set to `intent`
- `name`: Name(space) of the intent
- `required_slots`: Slots that must be filled, otherwise the intent cannot be parsed
  - `name`: Name of the slot (used in output and `utterances`)
  - `entity`: Entity type of the slot
- `optional_slots`: Slots that must not necessarily be filled. Parsing will not fail if the slot can not be filled, but the result will not contain a value for it in that case.
  - `name`: Name of the slot (used in output and `utterances`)
  - `entity`: Entity type of the slot
- `matching_strictness`: Controls how similar an utterance must be to the training data. Defaults to `0.0`
- `utterances`: A list of example utterances with slots in square brackets `[ ]`

### Dataset

You are free to organize the yaml documents as you want. Either having one yaml file for each intent and each entity, or gathering some documents together (e.g. all entities together, or all intents together) in the same yaml file. All files will be used together when generating the dataset. Here is the yaml file corresponding to the previous `city` entity and a `searchFlight` intent merged together:

```yaml
# city entity
---
type: entity
name: flights/entities/city
automatically_extensible: true
map_synonyms: true
values:
  - berlin
  - [new york, big apple]
  - tokyo

# searchFlight intent
---
type: intent
name: flights/intents/searchFlight
required_slots:
  - name: origin
    entity: flights/entities/city
  - name: destination
    entity: flights/entities/city
utterances:
  - find me a flight from [origin] to [destination]
  - I need a flight from [origin] to [destination]
  - show me flights to go to [destination] from [origin]
```

If you plan to have more than one entity or intent in a YAML file, you must separate them using the YAML document separator: `---`

Once your intents and entities are created using the YAML format described previously, you can produce a dataset using the [Command Line Interface (CLI)](cli.md):

```bash
python -m intently_nlu generate_dataset en dataset.yaml
```

Or alternatively, you can provide multiple YAML files to the [CLI](cli.md):

```bash
python -m intently_nlu generate_dataset en entities.yaml intents.yaml
```

This will generate a JSON dataset which can be used to train your engine.

## JSON format

The JSON format can be used to create datasets too, but it is not recommended because it does not support comments and it is less human-readable than the YAML format. It is also more verbose:

```json
{
  "entities": {
    "flights/entities/city": {
      "automatically_extensible": true,
      "map_synonyms": true,
      "matching_strictness": 0,
      "name": "flights/entities/city",
      "values": {
        "berlin": "berlin",
        "big apple": "new york",
        "new york": "new york",
        "tokyo": "tokyo"
      }
    }
  },
  "intents": {
    "flights/intents/searchFlight": {
      "matching_strictness": 0,
      "required_slots": {
        "destination": "flights/entities/city",
        "origin": "flights/entities/city"
      },
      "utterances": [
        "find me a flight from [origin] to [destination]",
        "I need a flight from [origin] to [destination]",
        "show me flights to go to [destination] from [origin]"
      ]
    }
  },
  "language": "en"
}
```

Once you have created a JSON dataset, either directly or with YAML files, you can use it to train an NLU engine. To do so, you can use the [CLI as documented here](cli.md), or the Python API.
