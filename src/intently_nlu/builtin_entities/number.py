"""Builtin number entity"""

import re
from typing import Any

from intently_nlu.dataset.dataset import Dataset
from intently_nlu.dataset.entity import Entity
from intently_nlu.dataset.intent import Intent
from intently_nlu.entity_parsers import EntityParser
from intently_nlu.exceptions import DatasetError
from intently_nlu.util.decorators.training import fitted_required, update_settings
from intently_nlu.util.intently_logging import get_logger, log_error
from intently_nlu.util.normalization import normalize


def get_number_entity():
    """Get number entity

    Returns:
        Entity: Number entity.
    """
    return Entity(
        name="intently/entities/number", values={"0": "0"}, automatically_extensible=True
    )


class NumberEntityParser(EntityParser):
    """Number entity parser."""

    def __init__(self):
        self.logger = get_logger(__name__)
        self.fitted = False
        self.settings = {"not_case_sensitive": True, "ignore_punctuation": True}
        self.slot = ""
        self.intent: Intent | None = None
        self.pattern: re.Pattern[str] | None
        self.lang = ""

    @update_settings
    def fit(
        self,
        dataset: Dataset,
        slot: str,
        intent: Intent,
        settings: dict[str, Any] | None = None,
    ) -> "NumberEntityParser":
        self.logger.debug("Fit NumberEntityParser...")

        self.slot = slot
        self.logger.debug(" Slot is %s", self.slot)
        self.intent = intent
        self.logger.debug(" Intent is %s", self.intent)

        self.lang = dataset.language
        self.logger.debug(" Language is %s", self.lang)

        if self.slot not in self.intent.all_slots:
            e = DatasetError(
                f"""Error while trying to fit NumberEntityParser:
                The slot {slot} is not in intent {self.intent.name}!"""
            )
            raise log_error(self.logger, e, "Fit NumberEntityParser") from e
        self.logger.debug(" Compile pattern...")
        self.pattern = re.compile(r"((-)?(\d+([,.]\d+)*))")
        self.logger.debug(" Compile pattern...Done!")
        self.fitted = True
        self.logger.debug("FitNumberEntityParser...Done!")
        return self

    @fitted_required
    def parse(self, text: str) -> tuple[str, float] | None:
        self.logger = get_logger(__name__)
        self.logger.debug("Parse...")
        if self.intent is None or self.pattern is None:
            self.logger.debug(" No intent!")
            self.logger.debug("Parse...Done!")
            return None
        parsed_slot: str | None = None

        self.logger.debug(" Try pattern...")
        result = re.search(
            self.pattern,
            normalize(
                string=text,
                to_lower_case=self.settings["not_case_sensitive"],
                try_remove_punctuation=self.settings["ignore_punctuation"],
                lang=self.lang,
            ),
        )
        if result is not None:
            parsed_slot = result.group()
        self.logger.debug(" Try pattern...Done!")
        if parsed_slot is None:
            self.logger.debug(" No match!")
            self.logger.debug("Parse...Done!")
            return None

        self.logger.debug(" Result: %s", (parsed_slot, 1.0))
        self.logger.debug("Parse...Done!")
        return (parsed_slot, 1.0)
