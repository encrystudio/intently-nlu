# Intently Natural Language Understanding (NLU)

[![PyPI - Version](https://img.shields.io/pypi/v/intently-nlu.svg)](https://pypi.org/project/intently-nlu)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/intently-nlu.svg)](https://pypi.org/project/intently-nlu)

Welcome to Intently NLU’s documentation.

Intently NLU is a Natural Language Understanding python library that allows to parse sentences written in natural language, and extract structured information. It is a fork of [Snips NLU](https://github.com/snipsco/snips-nlu).

The motivation of this project is to create a robust, fast and easy-to-use nlu library similar to [Snips NLU](https://github.com/snipsco/snips-nlu) with support for newer Python versions or tools, since [Snips NLU](https://github.com/snipsco/snips-nlu) has not been updated for a long time.

Let’s look at the following example, to illustrate the main purpose of this lib:

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

## About this documentation

This documentation is divided into different parts. It is recommended to start by the first two ones.

The [Installation](installation.md) part will get you set up. Then, the [Quickstart](quickstart.md) section will help you build an example.

After this, you can either start the [Tutorial](tutorial.md) which will guide you through the steps to create your own NLU engine and start parsing sentences, or you can alternatively check the [Key Concepts & Data Model](data_model.md) to know more about the NLU concepts used in this lib.

If you want to dive into the codebase or customize some parts, you can check the [github repository](https://github.com/encrystudio/intently-nlu).
