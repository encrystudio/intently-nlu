"""Abstract entity parser"""

from abc import ABC, abstractmethod
from typing import Any

from intently_nlu.dataset.dataset import Dataset
from intently_nlu.dataset.intent import Intent


class EntityParser(ABC):
    """Abstract entity parser which performs entity extraction/slot filling
    for one slot of one intent.

    A custom entity parser must inherit this class to be used in an `IntentlyNLUEngine`
    """

    @abstractmethod
    def fit(
        self,
        dataset: Dataset,
        slot: str,
        intent: Intent,
        settings: dict[str, Any] | None = None,
    ) -> "EntityParser":
        """Fit the entity parser with a valid IntentlyNLU `Dataset`

        Args:
            dataset (Dataset): Valid IntentlyNLU `Dataset`.
            slot (str): The name of the slot this parser will fill.
            intent (Intent): The `Intent` where the slot is from.
            settings (dict[str, Any], optional): Parser specific settings.
        """

    @abstractmethod
    def parse(self, text: str) -> tuple[str, float] | None:
        """Performs slot filling on the provided `text`

        Args:
            text (str): Text to perform slot filling on.

        Returns:
            tuple[str, float] | None: The parsed information with its probability.
        """
