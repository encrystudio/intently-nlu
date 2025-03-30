# Command Line Interface

The easiest way to test the abilities of the Intently NLU library is through the command line interface (CLI). The CLI is installed with the python package and is typically used by running `python -m intently_nlu <command> [args]`.

## Table of contents

- [Command Line Interface](#command-line-interface)
  - [Table of contents](#table-of-contents)
  - [Commands](#commands)
    - [Version](#version)
    - [Model Version](#model-version)
    - [Download Resources](#download-resources)
    - [Generate Dataset](#generate-dataset)
    - [Train Model](#train-model)
    - [Parsing](#parsing)
    - [Cleanup](#cleanup)

## Commands

### Version

To print the version of the library:

```bash
python -m intently_nlu version
>>> 0.0.2
```

### Model Version

To print the current model version:

```bash
python -m intently_nlu model-version
>>> 2
```

To print the model version of a specific trained model:

```bash
python -m intently_nlu model-version -p path/to/engine.inlue
>>> 2
```

### Download Resources

To download the resources for a specific [language](languages.md):

```bash
python -m intently_nlu download en
```

### Generate Dataset

To generate a JSON [dataset](dataset.md) from [intents](data_model.md#intent) and [entities](data_model.md#entities) YAML file(s):

```bash
python -m intently_nlu generate-dataset en path/to/first.yaml path/to/second.yaml
```

### Train Model

To train the model from a JSON [dataset](dataset.md):

```bash
python -m intently_nlu train path/to/dataset.json path/to/engine_out.inlue
```

### Parsing

To start parsing:

```bash
python -m intently_nlu parse path/to/engine.inlue
```

To parse a specific query:

```bash
python -m intently_nlu parse path/to/engine.inlue -q "Query to parse"
```

### Cleanup

To delete logs (flag `-l`) and remove downloaded resources (flag `-r`):

```bash
python -m intently_nlu cleanup -l -r
```
