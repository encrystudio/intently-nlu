# Installation

## Table of contents

- [Installation](#installation)
  - [Table of contents](#table-of-contents)
  - [System requirements](#system-requirements)
  - [Install Intently NLU](#install-intently-nlu)
  - [Language resources](#language-resources)

## System requirements

| Symbol             | Meaning                       |
| ------------------ | ----------------------------- |
| :white_check_mark: | Tested / Stable / Recommended |
| :grey_question:    | Not tested                    |
| :x:                | Not supported                 |

| OS                | Status             |
| ----------------- | ------------------ |
| Android           | :grey_question:    |
| Linux             | :grey_question:    |
| MacOS             | :grey_question:    |
| Raspberry Pi OS   | :grey_question:    |
| Windows 10 64-bit | :white_check_mark: |
| Windows (other)   | :grey_question:    |

| Python version | Status             |
| -------------- | ------------------ |
| Python > 3.13  | :grey_question:    |
| Python 3.13    | :white_check_mark: |
| Python 3.12    | :white_check_mark: |
| Python 3.11    | :white_check_mark: |
| Python 3.10    | :white_check_mark: |
| Python < 3.10  | :x:                |

## Install Intently NLU

It is recommended to use a [virtual environment](https://virtualenv.pypa.io) and activate it before installing Intently NLU in order to manage your project dependencies properly.

Intently NLU can be installed via pip with the following command:

`python -m pip install intently-nlu`

or

`python3 -m pip install intently-nlu`

or

`py -m pip install intently-nlu`

We currently do not provide any pre-built binaries (wheels) for intently-nlu and its dependencies. You will need to build intently-nlu and its dependencies from sources which means maybe you will need to install additional build tools before running the `pip install` command.

## Language resources

Intently NLU relies on [language resources](https://github.com/encrystudio/intently-nlu/tree/main/resources/languages) which must be downloaded separately. To fetch the resources for a specific language, run the following command:

`python -m intently_nlu download <language>`

For more information, run `python -m intently_nlu download -h`.

The list of supported languages is described [here](languages.md).
