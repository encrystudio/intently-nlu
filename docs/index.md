# Intently NLU

[![PyPI - Version](https://img.shields.io/pypi/v/intently-nlu.svg)](https://pypi.org/project/intently-nlu)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/intently-nlu.svg)](https://pypi.org/project/intently-nlu)

Intently NLU is a Python library that allows to extract the intention and structured information from sentences written in natural language.

## Table of Contents

- [Intently NLU](#intently-nlu)
  - [Table of Contents](#table-of-contents)
  - [State](#state)
  - [About](#about)
  - [Getting Started](#getting-started)
  - [API Usage](#api-usage)
  - [Sample datasets](#sample-datasets)
  - [Documentation](#documentation)
  - [Contributing](#contributing)
  - [License](#license)

## State

Currently in phase 1: planning
Documentation is missing or not complete!

## About

Behind every chatbot and voice assistant lies a common piece of technology: Natural Language Understanding (NLU). Anytime a user interacts with an assistant using natural language, their words need to be translated into a machine-readable description of what they meant.

The NLU engine first detects what the intention of the user is (a.k.a. intent), then extracts the parameters (called slots) of the query. The developer can then use this to determine the appropriate action or response.

Let’s take an example to illustrate this, and consider the following sentence:

`"What will be the weather in berlin at 9pm?"`

Properly trained, the Intently NLU engine will be able to extract structured data such as:

```json
{
  "intent": "weather/intents/searchWeatherForecast",
  "probability": 0.95,
  "raw_utterance": "What will be the weather in berlin at 9pm?",
  "resolved_slots": {
    "locality": "berlin",
    "forecast_start_datetime": "9pm"
  }
}
```

In this case, the identified intent is `weather/intents/searchWeatherForecast` and two slots were extracted, a locality and a time.

This library is highly inspired by and forked from [Snips NLU](https://github.com/snipsco/snips-nlu), although large parts of the library have been completely rewritten or restructured. Therefore, not all functionality of [Snips NLU](https://github.com/snipsco/snips-nlu) is available in the same way, some are even missing completely.

The motivation of this project is to create a robust, fast and easy-to-use nlu library similar to [Snips NLU](https://github.com/snipsco/snips-nlu) with support for newer Python versions or tools, since [Snips NLU](https://github.com/snipsco/snips-nlu) has not been updated for a long time.

## Getting Started

TODO

## API Usage

TODO

## Sample datasets

Here is a list of some datasets that can be used to train am Intently NLU engine:

- [Smarthome dataset](examples/example.json): "Set the temperature to 18 degrees in the bedroom", "Turn off the lights in the living room"

## Documentation

TODO

## Contributing

TODO

## License

The whole library is built using many concepts from [Snips NLU](https://github.com/snipsco/snips-nlu),
which is licensed under [Apache License, Version 2.0](https://opensource.org/license/apache-2-0).
The library itself is licensed under [Apache License, Version 2.0](https://opensource.org/license/apache-2-0) too.

`intently-nlu` is provided as Open Source software. See [LICENSE](LICENSE) and [NOTICE](NOTICE) for more information.
