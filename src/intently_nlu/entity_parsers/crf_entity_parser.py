"""Conditional random field-based entity parser"""

from typing import Any

import sklearn_crfsuite  # type: ignore

from intently_nlu.constants import NONE_LABEL
from intently_nlu.dataset.dataset import Dataset
from intently_nlu.dataset.intent import Intent
from intently_nlu.exceptions import DatasetError
from intently_nlu.util.decorators.training import fitted_required, update_settings
from intently_nlu.util.intently_logging import get_logger, log_error
from intently_nlu.util.ml_training import (
    sentence_to_features,
    utterance_data_augmentation,
)

from .entity_parser import EntityParser


class CRFEntityParser(EntityParser):
    """Conditional random field-based entity parser"""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.fitted = False
        self.settings = {"not_case_sensitive": True, "ignore_punctuation": True}
        self.slot = ""
        self.intent: Intent | None = None
        self.lang = ""
        self.crf: sklearn_crfsuite.CRF | None = None

    @update_settings
    def fit(
        self,
        dataset: Dataset,
        slot: str,
        intent: Intent,
        settings: dict[str, Any] | None = None,
    ) -> "CRFEntityParser":
        self.logger.debug("Fit CRFEntityParser...")

        self.slot = slot
        self.logger.debug(" Slot is %s", self.slot)
        self.intent = intent
        self.logger.debug(" Intent is %s", self.intent)

        self.lang = dataset.language
        self.logger.debug(" Language is %s", self.lang)

        if self.slot not in self.intent.all_slots:
            e = DatasetError(
                f"""Error while trying to fit CRFEntityParser:
                The slot {slot} is not in intent {self.intent.name}!"""
            )
            raise log_error(self.logger, e, "Fit CRFEntityParser") from e
        self.logger.debug(" Augment data...")
        augmented_data = utterance_data_augmentation(
            intent.utterances, intent.all_slots
        )
        train_sentences = [sentence for sentence, _ in augmented_data]
        train_labels = [labels for _, labels in augmented_data]

        x_train = [sentence_to_features(sent) for sent in train_sentences]
        y_train = train_labels
        self.logger.debug(" Augment data...Done!")
        self.logger.debug(" Fit CRF model...")
        self.crf = sklearn_crfsuite.CRF(
            algorithm="lbfgs",  # TODO: try accuracy and performance of "arow" and "l2sgd" instead of "lbfgs"
            c1=0.1,
            c2=0.1,
            max_iterations=100,
            all_possible_transitions=True,
        )
        self.crf.fit(x_train, y_train)  # type: ignore
        self.logger.debug(" Fit CRF model...Done!")
        self.fitted = True
        self.logger.debug("Fit CRFEntityParser...Done!")
        return self

    @fitted_required
    def parse(self, text: str) -> tuple[str, float] | None:
        self.logger = get_logger(__name__)
        self.logger.debug("Parse...")
        if self.intent is None:
            self.logger.debug(" No intent!")
            self.logger.debug("Parse...Done!")
            return None
        if self.crf is None:
            self.logger.debug(" No CRF model!")
            self.logger.debug("Parse...Done!")
            return None
        parsed_slot: str | None = None

        self.logger.debug(" Run model...")
        split_utterance = text.strip().split()
        x = [sentence_to_features(split_utterance)]
        predicted_labels: list[str] = self.crf.predict(x)[0].tolist()  # type: ignore
        probabilities = self.crf.predict_marginals(x)[0]  # type: ignore
        probs = [
            probabilities[i][predicted_labels[i]]
            for i in range(len(predicted_labels))
            if predicted_labels[i] != NONE_LABEL
        ]
        overall_prob = sum(probs) / len(probs) if probs else 0.0
        self.logger.debug(" Run model...Done!")
        self.logger.debug(" Model prediction: %s", predicted_labels)
        if not self.slot in predicted_labels:
            probabilities = self.crf.predict_marginals(x)[0]  # type: ignore
            min_confidence_index = min(
                range(len(predicted_labels)),
                key=lambda i: probabilities[i][predicted_labels[i]],
            )
            overall_prob = probabilities[min_confidence_index][self.slot]
            self.logger.debug(
                " Replace label with least confidence: %s",
                split_utterance[min_confidence_index],
            )
            predicted_labels[min_confidence_index] = self.slot

        slot_tokens = [
            token
            for token, label in zip(split_utterance, predicted_labels)
            if label == self.slot
        ]
        parsed_slot = " ".join(slot_tokens) if slot_tokens else None
        if not parsed_slot:
            return None

        if (
            not self.intent.all_slots[self.slot].automatically_extensible
        ) and not parsed_slot in self.intent.all_slots[self.slot].values:
            self.logger.debug(" Match not in training data!")
            self.logger.debug("Parse...Done!")
            return None

        if self.intent.all_slots[self.slot].map_synonyms:
            return (
                (self.intent.all_slots[self.slot].values[parsed_slot], overall_prob)
                if parsed_slot in self.intent.all_slots[self.slot].values
                else (parsed_slot, overall_prob)
            )

        self.logger.debug(" Result: %s", (parsed_slot, overall_prob))
        self.logger.debug("Parse...Done!")
        return (parsed_slot, overall_prob)
