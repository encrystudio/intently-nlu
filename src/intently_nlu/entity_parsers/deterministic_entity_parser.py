"""Deterministic entity parser"""

import re
from typing import Any

from intently_nlu.dataset.dataset import Dataset
from intently_nlu.dataset.intent import Intent
from intently_nlu.exceptions import DatasetError
from intently_nlu.util.decorators.training import fitted_required, update_settings
from intently_nlu.util.intently_logging import get_logger, log_error
from intently_nlu.util.normalization import normalize

from .entity_parser import EntityParser


class DeterministicEntityParser(EntityParser):
    """Deterministic entity parser that uses a single pattern"""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.fitted = False
        self.settings = {"not_case_sensitive": True, "ignore_punctuation": True}
        self.slot = ""
        self.intent: Intent | None = None
        self.pattern: list[str] = []
        self.lang = ""

    @update_settings
    def fit(
        self,
        dataset: Dataset,
        slot: str,
        intent: Intent,
        settings: dict[str, Any] | None = None,
    ) -> "DeterministicEntityParser":
        self.logger.debug("Fit DeterministicEntityParser...")

        self.slot = slot
        self.logger.debug(" Slot is %s", self.slot)
        self.intent = intent
        self.logger.debug(" Intent is %s", self.intent)

        self.lang = dataset.language
        self.logger.debug(" Language is %s", self.lang)

        if self.slot not in self.intent.all_slots:
            e = DatasetError(
                f"""Error while trying to fit DeterministicEntityParser:
                The slot {slot} is not in intent {self.intent.name}!"""
            )
            raise log_error(self.logger, e, "Fit DeterministicEntityParser") from e

        def utterance_to_regex_pattern(utterance: str) -> str:
            return re.sub(
                r"\[.*?\]",
                ".*",
                re.escape(utterance).replace(re.escape(f"[{slot}]"), r"(.*)"),
            ).replace("\\.*", ".*")

        self.logger.debug(" Generate patterns...")
        for utterance in intent.utterances:
            if f"[{slot}]" in utterance:
                self.pattern.append(
                    utterance_to_regex_pattern(
                        normalize(
                            utterance,
                            to_lower_case=self.settings["not_case_sensitive"],
                            try_remove_punctuation=self.settings["ignore_punctuation"],
                            lang=self.lang,
                        )
                    )
                )
        self.logger.debug(" Generate patterns...Done!")
        if not self.pattern:
            e = DatasetError(
                f"""Error while trying to fit DeterministicEntityParser:
                No given utterance of intent {self.intent.name} contains slot {slot}!"""
            )
            raise log_error(self.logger, e, "Fit DeterministicEntityParser") from e

        self.fitted = True
        self.logger.debug("Fit DeterministicEntityParser...Done!")
        return self

    @fitted_required
    def parse(self, text: str) -> tuple[str, float] | None:
        self.logger = get_logger(__name__)
        self.logger.debug("Parse...")
        if self.intent is None:
            self.logger.debug(" No intent!")
            self.logger.debug("Parse...Done!")
            return None
        parsed_slot: str | None = None

        self.logger.debug(" Try patterns...")
        for pattern in self.pattern:
            result = re.search(
                pattern,
                normalize(
                    string=text,
                    to_lower_case=self.settings["not_case_sensitive"],
                    try_remove_punctuation=self.settings["ignore_punctuation"],
                    lang=self.lang,
                ),
            )
            if result is not None:
                parsed_slot = str(result.group(1))
                if self.intent.all_slots[self.slot].automatically_extensible:
                    break
                if parsed_slot in self.intent.all_slots[self.slot].values:
                    break
                parsed_slot = None
        self.logger.debug(" Try patterns...Done!")
        if parsed_slot is None:
            self.logger.debug(" No match!")
            self.logger.debug("Parse...Done!")
            return None
        if (
            not self.intent.all_slots[self.slot].automatically_extensible
        ) and not parsed_slot in self.intent.all_slots[self.slot].values:
            self.logger.debug(" Match not in training data!")
            self.logger.debug("Parse...Done!")
            return None
        if self.intent.all_slots[self.slot].map_synonyms:
            return (
                (self.intent.all_slots[self.slot].values[parsed_slot], 1.0)
                if parsed_slot in self.intent.all_slots[self.slot].values
                else (parsed_slot, 1.0)
            )

        self.logger.debug(" Result: %s", (parsed_slot, 1.0))
        self.logger.debug("Parse...Done!")
        return (parsed_slot, 1.0)
