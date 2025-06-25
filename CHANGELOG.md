<!-- markdownlint-disable MD024 -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

- [Changelog](#changelog)
  - [\[0.0.3\] - 2025-03-30](#003---2025-03-30)
    - [Added](#added)
    - [Changed](#changed)
    - [Fixed](#fixed)
  - [\[0.0.2\] - 2025-03-30](#002---2025-03-30)
    - [Added](#added-1)
    - [Changed](#changed-1)
    - [Removed](#removed)
    - [Fixed](#fixed-1)
  - [\[0.0.1\] - 2025-02-10](#001---2025-02-10)

## [0.0.3] - 2025-03-30

### Added

- information to `README.md`
- information to `pyproject.toml`
- support for entities with more than one word in `crf_entity_parser.py`
- `CHANGELOG.md`

### Changed

- theme of documentation
- from `Planning` to `Pre-Alpha`
- `fuzzy_intent_classifier.py` to consider `token_sort_ratio` _and_ `ratio` instead of _just_ `ratio`
- updated dependencies

### Fixed

- some documentation issues
- some type issues
- fixed bug where sometimes a false intent is classified when two intents are too similar in `fuzzy_intent_classifier.py`

## [0.0.2] - 2025-03-30

### Added

- theme to documentation
- pages to documentation
- completed information in `__about__.py`
- `as_json()` method to `IntentlyNLUResult` class

### Changed

- persisted engine file naming and versioning

### Removed

- different pt languages

### Fixed

- `fitted_required` annotation

## [0.0.1] - 2025-02-10

- initial release
