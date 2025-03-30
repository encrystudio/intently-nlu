# Key Concepts & Data Model

This section is meant to explain the concepts and data model that we use to represent input and output data.

The main task that this lib performs is _Information Extraction_, or _Intent Parsing_, to be even more specific. At this point, the output of the engine may still not be very clear to you.

The task of parsing intents is actually two-folds. The first step is to understand which intent the sentence is about. The second step is to extract the parameters, a.k.a. the _slots_ of the sentence.

## Table of contents

- [Key Concepts \& Data Model](#key-concepts--data-model)
  - [Table of contents](#table-of-contents)
  - [Intent](#intent)
  - [Slot](#slot)
  - [Slot type vs. slot name](#slot-type-vs-slot-name)
  - [Entities](#entities)
    - [Builtin Entities](#builtin-entities)
    - [Entity Values \& Synonyms](#entity-values--synonyms)
    - [Automatically Extensible Entities](#automatically-extensible-entities)

## Intent

In the context of information extraction, an _intent_ corresponds to the action or intention contained in the user’s query, which can be more or less explicit.

Lets’ consider for instance the following sentences:

```python
"Turn on the light"
"It's too dark in this room, can you fix this?"
```

They both express the same intent which is `switchLightOn`, but they are expressed in two very different ways.

Thus, the first task in intent parsing is to be able to detect the _intent_ of the sentence, or say differently to classify sentences based on their underlying _intent_.

In Intently NLU, this is represented within the parsing output in this way:

```json
{
  "intent": "turnLightOn",
  "probability": 0.8421052631578947
}
```

So you have an additional information which is the probability that the extracted intent correspond to the actual one.

## Slot

The second part of the task, once the intent is known, is to extract the parameters that may be contained in the sentence. We called them _slots_.

For example, let’s consider this sentence:

```python
"Turn on the light in the kitchen"
```

As before the intent is `switchLightOn`, however there is now an additional piece of information which is contained in the word `kitchen`.

This intent contains one slot, which is the _room_ in which the light is to be turned on.

Let’s consider another example:

```python
"Find me a flight from Berlin to Tokyo"
```

Here the intent would be `searchFlight`, and now there are two slots in the sentence being contained in "Berlin" and "Tokyo". These two values are of the same type as they both correspond to a location however they have different roles, as Berlin is the **departure** and Tokyo is the **arrival**.

In this context, we call **location** a _slot type_ (or _entity_) and **departure** and **arrival** are _slot names_.
_Slot type_ and _entity_ are [synonyms](#entity-values--synonyms).

## Slot type vs. slot name

A slot type or entity is to NLU what a type is to coding. It describes the nature of the value. In a piece of code, multiple variables can be of the same type while having different purposes, usually transcribed in their name. All variables of a same type will have some common characteristics, for instance they have the same methods, they may be comparable etc.

In information extraction, a slot type corresponds to a class of values that fall into the same category. In our previous example, the **location** slot type corresponds to all values that correspond to a place, a city, a country or anything that can be located.

The slot name can be thought as the role played by the entity in the sentence.

In Intently NLU, extracted slots are represented within the output in this way:

```json
{
  "resolved_slots": {
    "departure": "Berlin",
    "arrival": "Tokyo"
  }
}
```

## Entities

### Builtin Entities

Currently we have one builtin entity, `intently/entities/number`. You can use it in your intents without any extra configuration.

### Entity Values & Synonyms

The first thing you can do is add a list of possible values for your entity.

By providing a list of example values for your entity, you help Intently NLU grasp what the entity is about.

Let’s say you are creating an assistant whose purpose is to let you set the color of your connected light bulbs. What you will do is define a `color` entity. On top of that you can provide a list of sample colors by editing the entity in your dataset as follows:

```yaml
---
type: entity
name: color
values:
  - white
  - yellow
  - pink
  - blue
```

Now imagine that you want to allow some variations around these values e.g. using `"pinky"` instead of `"pink"`. You could add these variations in the list by adding a new value, however in this case what you want is to tell the NLU to consider `"pinky"` as a _synonym_ of `"pink"`:

```yaml
---
type: entity
name: color
map_synonyms: yes
values:
  - white
  - yellow
  - [pink, pinky]
  - blue
```

In this context, Intently NLU will map `"pinky"` to its reference value, `"pink"`, in its output, because `map_synonyms` is true (default is false).

Let’s consider this sentence:

```python
"Please make the light pinky"
```

Here is the kind of NLU output that you would get in this context:

```json
{
  "intent": "setLightColor",
  "probability": 0.95,
  "raw_utterance": "Please make the light pinky",
  "resolved_slots": {
    "color": "pink"
  }
}
```

The actual value of `color` would be `"pinky"`, but it has been resolved and it contains the reference color, `"pink"`, that the synonym refers to.

### Automatically Extensible Entities

On top of declaring color values and color synonyms, you can also decide how Intently NLU reacts to unknown entity values.

In the light color assistant example, one of the first things to do would be to check what are the colors that are supported by the bulb, for instance:

```json
["white", "yellow", "red", "blue", "green", "pink", "purple"]
```

As you can only handle these colors, you can enforce Intently NLU to filter out slot values that are not part of this list, so that the output always contain valid values, i.e. supported colors.

On the contrary, let’s say you want to build a smart music assistant that will let you control your speakers and play any artist you want.

Obviously, you can’t list all the artist and songs that you might want to listen to at some point. This means that your dataset will contain some examples of such artist but you expect Intently NLU to extend beyond these values and extract any other artist or song that appear in the same context.

Your entity must be _automatically extensible_.

Now in practice, there is a flag in the dataset that lets you choose whether or not your custom entity is automatically extensible (false by default):

```yaml
---
type: entity
name: my_custom_entity
automatically_extensible: yes
```
