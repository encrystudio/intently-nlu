"""Deterministic intent classifier"""

import re
from typing import Any

from intently_nlu.dataset.dataset import Dataset
from intently_nlu.dataset.intent import Intent
from intently_nlu.util.decorators.training import fitted_required, update_settings
from intently_nlu.util.intently_logging import get_logger
from intently_nlu.util.normalization import normalize

from .intent_classifier import IntentClassifier


class DeterministicIntentClassifier(IntentClassifier):
    """Intent classifier using pattern matching in a deterministic manner

    This intent classifier is very strict by nature, and tends to have a very good
    precision but a low flexibility.
    """

    def __init__(self):
        self.logger = get_logger(__name__)
        self.fitted = False
        self.settings = {"not_case_sensitive": True, "remove_punctuation": True}
        self.intents: dict[str, Intent] = {}
        self.intent_pattern: dict[re.Pattern[str], str] = {}
        self.language = ""

    @update_settings
    def fit(
        self,
        dataset: Dataset,
        settings: dict[str, Any] | None = None,
    ) -> None:
        self.logger.debug("Fit DeterministicIntentParser...")
        self.intents = dataset.intents
        self.logger.debug(" Intents: %s", self.intents)
        self.language = dataset.language

        def utterance_to_regex_pattern(utterance: str) -> re.Pattern[str]:
            # Convert the slots "[*]" to a regex pattern that matches any sequence of words
            return re.compile(re.sub(r"\[.*?\]", "(.*)", utterance))

        self.logger.debug(" Generate patterns...")
        for intent in self.intents.items():
            for utterance in intent[1].utterances:
                self.intent_pattern[
                    utterance_to_regex_pattern(
                        normalize(
                            utterance,
                            try_remove_punctuation=self.settings["remove_punctuation"],
                            to_lower_case=self.settings["not_case_sensitive"],
                            lang=self.language,
                        )
                    )
                ] = intent[0]
        self.logger.debug(" Generate patterns...Done!")
        self.logger.debug("Fit DeterministicIntentParser...Done!")
        self.fitted = True

    @fitted_required
    def classify(self, text: str) -> tuple[Intent, float] | None:
        self.logger = get_logger(__name__)
        self.logger.debug("Classify...")
        for utterance_pattern in list(self.intent_pattern.keys()):
            is_match = re.fullmatch(
                utterance_pattern,
                normalize(
                    text,
                    try_remove_punctuation=self.settings["remove_punctuation"],
                    to_lower_case=self.settings["not_case_sensitive"],
                    lang=self.language,
                ),
            )
            if is_match:
                self.logger.debug(
                    " Match: %s",
                    (self.intents[self.intent_pattern[utterance_pattern]], 1.0),
                )
                self.logger.debug("Classify...Done!")
                return (self.intents[self.intent_pattern[utterance_pattern]], 1.0)
        self.logger.debug(" No match")
        self.logger.debug("Classify...Done!")
        return None

    @fitted_required
    def classify_all(self, text: str) -> list[tuple[Intent, float]] | None:
        self.logger = get_logger(__name__)
        self.logger.debug("Classify all...")
        parsed_intents: list[tuple[Intent, float]] = []

        for utterance_pattern in list(self.intent_pattern.keys()):
            is_match = re.fullmatch(
                utterance_pattern,
                normalize(
                    text,
                    try_remove_punctuation=self.settings["remove_punctuation"],
                    to_lower_case=self.settings["not_case_sensitive"],
                    lang=self.language,
                ),
            )
            if is_match:
                self.logger.debug(
                    " Match: %s",
                    (self.intents[self.intent_pattern[utterance_pattern]], 1.0),
                )
                parsed_intents.append(
                    (self.intents[self.intent_pattern[utterance_pattern]], 1.0)
                )

        if not parsed_intents:
            self.logger.debug(" No match")
            self.logger.debug("Classify all...Done!")
            return None
        self.logger.debug(" Parsed intents: %s", parsed_intents)
        self.logger.debug("Classify all...Done!")
        return parsed_intents
