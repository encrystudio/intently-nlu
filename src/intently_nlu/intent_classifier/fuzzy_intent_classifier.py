"""Fuzzy intent classifier"""

import re
from typing import Any

from rapidfuzz import fuzz

from intently_nlu.dataset.dataset import Dataset
from intently_nlu.dataset.intent import Intent
from intently_nlu.util.decorators.training import fitted_required, update_settings
from intently_nlu.util.intently_logging import get_logger
from intently_nlu.util.normalization import normalize

from .intent_classifier import IntentClassifier


class FuzzyIntentClassifier(IntentClassifier):
    """Intent parser that uses the `RapidFuzz` library
    It calculates the 'Levenshtein Distance' between each utterance from the dataset and the input utterance.

    This intent parser is medium strict, and tends to have a good precision with medium flexibility.
    """

    def __init__(self):
        self.logger = get_logger(__name__)
        self.fitted = False
        self.settings = {"not_case_sensitive": True, "remove_punctuation": True}
        self.intents: dict[str, Intent] = {}
        self.normalized_intent_utterances: dict[str, Intent] = {}
        self.language = ""

    def _normalized(self, text: str) -> str:
        """Normalizes a given text and removes slots.

        Args:
            text (str): The text to be normalized.

        Returns:
            str: Normalized text.
        """
        text = re.sub(r"\[.*?\]", "", text)
        text = normalize(
            text,
            to_lower_case=self.settings["not_case_sensitive"],
            try_remove_punctuation=self.settings["remove_punctuation"],
            lang=self.language,
        )
        return text

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
        for intent in list(self.intents.values()):
            for utterance in intent.utterances:
                self.normalized_intent_utterances[self._normalized(utterance)] = intent
        self.logger.debug("Utterances: %s", self.normalized_intent_utterances)
        self.fitted = True

    @fitted_required
    def classify(self, text: str) -> tuple[Intent, float] | None:
        self.logger = get_logger(__name__)
        self.logger.debug("Classify...")
        best_match: Intent | None = None
        best_score = 0.0
        normalized_text = self._normalized(text)

        for utterance, intent in self.normalized_intent_utterances.items():
            ratio1 = fuzz.ratio(normalized_text, utterance)
            ratio2 = fuzz.token_sort_ratio(normalized_text, utterance)
            ratio = (ratio1 + ratio2) / 2 / 100
            if ratio > best_score:
                best_match = intent
                best_score = ratio

        if best_match is None:
            self.logger.debug(" No match")
            self.logger.debug("Classify...Done!")
            return None
        self.logger.debug(" Best match: %s", (best_match, best_score))
        self.logger.debug("Classify...Done!")
        return (best_match, best_score)

    @fitted_required
    def classify_all(self, text: str) -> list[tuple[Intent, float]] | None:
        self.logger = get_logger(__name__)
        self.logger.debug("Classify all...")
        parsed_intents: list[tuple[Intent, float]] = []
        normalized_text = self._normalized(text)

        for utterance, intent in self.normalized_intent_utterances.items():
            ratio1 = fuzz.ratio(normalized_text, utterance)
            ratio2 = fuzz.token_sort_ratio(normalized_text, utterance)
            ratio = (ratio1 + ratio2) / 2 / 100
            parsed_intents.append((intent, ratio))

        if not parsed_intents:
            self.logger.debug(" No match")
            self.logger.debug("Classify all...Done!")
            return None
        self.logger.debug(" Parsed intents: %s", parsed_intents)
        self.logger.debug("Classify all...Done!")
        return parsed_intents
