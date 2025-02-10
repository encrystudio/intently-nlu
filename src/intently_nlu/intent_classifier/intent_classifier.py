"""Abstract intent classifier"""

from abc import ABC, abstractmethod
from typing import Any

from intently_nlu.dataset.dataset import Dataset
from intently_nlu.dataset.intent import Intent


class IntentClassifier(ABC):
    """Abstract intent classifier which performs intent classification

    A custom intent classifier must inherit this class to be used in an `IntentlyNLUEngine`
    """

    @abstractmethod
    def fit(
        self,
        dataset: Dataset,
        settings: dict[str, Any] | None = None,
    ) -> None:
        """Fit the intent classifier with a valid IntentlyNLU `Dataset`

        Args:
            dataset (Dataset): Valid IntentlyNLU `Dataset`.
            settings (dict[str, Any], optional): Classifier specific settings.
        """

    @abstractmethod
    def classify(self, text: str) -> tuple[Intent, float] | None:
        """Performs intent classification on the provided `text`

        Args:
            text (str): Text to perform classification on.

        Returns:
            tuple[Intent, float] | None: The best matching `Intent` with its probability.
        """

    @abstractmethod
    def classify_all(self, text: str) -> list[tuple[Intent, float]] | None:
        """Performs intent classification on the provided `text` like `IntentParser.classify()`,
           but returns a list of intents ordered by decreasing probability with their matching probability

        Args:
            text (str): Text to perform classification on.

        Returns:
            list[tuple[Intent, float]] | None: The `Intent`s ordered by decreasing probability with their matching probability.
        """
