"""IntentlyNLU Engine configuration"""

from dataclasses import dataclass, field
from typing import Any

from intently_nlu.constants import ENTITY_PARSERS, INTENT_CLASSIFIERS
from intently_nlu.entity_parsers import (
    BUILTIN_ENTITY_PARSERS,
    CRFEntityParser,
    DeterministicEntityParser,
    EntityParser,
)
from intently_nlu.intent_classifier import (
    BUILTIN_INTENT_CLASSIFIERS,
    DeterministicIntentClassifier,
    FuzzyIntentClassifier,
    IntentClassifier,
)


@dataclass(frozen=True)
class IntentlyNLUEngineConfig:
    """Configuration of an `IntentlyNLUEngine`

    Args:
        intent_classifiers (list[IntentClassifier]): List of intent classifiers.
                                                     The order in the list determines the order in which
                                                     each parser will be called by the `IntentlyNLUEngine`.
        entity_parsers (list[EntityParser]): List of entity parsers that will be trained and used to extract entities.

    """

    intent_classifiers: list[IntentClassifier] = field(
        default_factory=lambda: [
            DeterministicIntentClassifier(),
            FuzzyIntentClassifier(),
        ]
    )
    entity_parsers: list[type[EntityParser]] = field(
        default_factory=lambda: [DeterministicEntityParser, CRFEntityParser]
    )

    @classmethod
    def from_json(
        cls,
        json: dict[str, Any],
        additional_classifiers: dict[str, type[IntentClassifier]] | None = None,
        additional_parsers: dict[str, type[EntityParser]] | None = None,
    ) -> "IntentlyNLUEngineConfig":
        """Parses the config from a JSON file

        Args:
            json (dict[str, Any]): JSON file as a dictionary.
            additional_classifiers (dict[str, type[IntentClassifier]], optional): Custom or plugin classifiers.
            additional_parsers (dict[str, type[EntityParser]], optional): Custom or plugin parsers.

        Returns:
            IntentlyNLUEngineConfig: The parsed config.
        """
        classifiers_in_scope = BUILTIN_INTENT_CLASSIFIERS.copy()
        parsers_in_scope = BUILTIN_ENTITY_PARSERS.copy()

        if additional_classifiers:
            classifiers_in_scope = classifiers_in_scope | additional_classifiers

        if additional_parsers:
            parsers_in_scope = parsers_in_scope | additional_parsers

        intent_classifiers: list[IntentClassifier] = []
        entity_parsers: list[type[EntityParser]] = []

        for classifier in json[INTENT_CLASSIFIERS]:
            if classifier in classifiers_in_scope:
                intent_classifiers.append(classifiers_in_scope[classifier]())

        for parser in json[ENTITY_PARSERS]:
            if parser in parsers_in_scope:
                entity_parsers.append(parsers_in_scope[parser])

        return IntentlyNLUEngineConfig(intent_classifiers, entity_parsers)
