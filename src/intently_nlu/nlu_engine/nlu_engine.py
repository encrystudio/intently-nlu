"""The main engine"""

import os

import dill  # type: ignore

from intently_nlu.__about__ import __model_version__
from intently_nlu.builtin_entities import BUILTIN_ENTITY_ENTITY_PARSERS
from intently_nlu.dataset.dataset import Dataset, Entity
from intently_nlu.dataset.intent import Intent
from intently_nlu.entity_parsers import EntityParser
from intently_nlu.exceptions import DatasetNotValid
from intently_nlu.nlu_engine.nlu_engine_config import IntentlyNLUEngineConfig
from intently_nlu.nlu_engine.nlu_result import IntentlyNLUResult
from intently_nlu.util.decorators.timing import elapsed_time
from intently_nlu.util.decorators.training import fitted_required
from intently_nlu.util.intently_logging import get_logger, log_error


class IntentlyNLUEngine:
    """Main class to use for intent classification and slot filling

    The NLU engine can be configured by passing an `IntentlyNLUEngineConfig`.

    An `IntentlyNLUEngine` relies on a list of `IntentClassifier`
    objects to classify intents, by calling them all and using the highest
    probability score.

    With the default parameters, it will use the two following intent classifiers
    in this order:

    - a `.DeterministicIntentClassifier`
    - a `.FuzzyIntentClassifier`

    The logic behind is to first use a conservative classifier which has a very
    good precision while its flexibility is moderate, so simple patterns will be
    caught, and then fallback on a second classifier which is based on similarity
    and will be able to classify some unseen utterances while ensuring a good
    precision.

    An `IntentlyNLUEngine` also relies on a list of `EntityParser`
    objects to parse entities for slot filling, by calling only the required ones.
    """

    def __init__(self, config: IntentlyNLUEngineConfig | None = None):
        self.logger = get_logger(__name__)
        self.config = config if config else IntentlyNLUEngineConfig()
        self.intent_classifiers = self.config.intent_classifiers
        self.intents: dict[str, Intent] = {}
        self.entity_parsers: dict[str, dict[str, list[EntityParser]]] = {}
        self.entity_parsers_per_slot: list[type[EntityParser]] = (
            self.config.entity_parsers
        )
        self.language: str = ""
        self.fitted = False
        self.logger.debug("Instance of `IntentlyNLUEngine` created: %s", self)

    @elapsed_time("Engine fitted in", warn_if_more_than=1)
    def fit(self, dataset: Dataset) -> "IntentlyNLUEngine":
        """Fit the NLU engine

        Args:
            dataset (Dataset): Valid IntentlyNLU `Dataset`.

        Raises:
            DatasetNotValid: Raised if the `Dataset` is not valid.

        Returns:
            IntentlyNLUEngine: Returns the fitted engine (self).
        """
        self.logger.debug("Fit...")
        if not dataset.is_valid:
            self.logger.error("Dataset could not be validated.")
            e = DatasetNotValid("Dataset could not be validated.")
            raise log_error(self.logger, e, "Fit engine") from e
        self.logger.debug(" Dataset validated.")
        self.language = dataset.language
        self.logger.debug(" Language: %s", self.language)
        for intent_name in dataset.intents:
            self.intents[intent_name] = dataset.intents[intent_name]
        self.logger.debug(" Fit intent classifiers...")
        for intent_classifier in self.intent_classifiers:
            intent_classifier.fit(dataset)
        self.logger.debug(" Fit intent classifiers...Done!")
        self.logger.debug(" Fit entity parsers...")
        for intent in self.intents.values():
            for slot, entity in intent.required_slots.items():
                if intent.name not in self.entity_parsers:
                    self.entity_parsers[intent.name] = {}
                self.entity_parsers[intent.name][slot] = []
                if entity.is_builtin:
                    self.entity_parsers[intent.name][slot].append(
                        BUILTIN_ENTITY_ENTITY_PARSERS[entity.name]().fit(
                            dataset, slot, intent
                        )
                    )
                else:
                    for parser in self.entity_parsers_per_slot:
                        self.entity_parsers[intent.name][slot].append(
                            parser().fit(dataset, slot, intent)
                        )
            for slot, entity in (
                intent.optional_slots.items()
                if intent.optional_slots
                else dict[str, Entity]().items()
            ):
                if intent.name not in self.entity_parsers:
                    self.entity_parsers[intent.name] = {}
                self.entity_parsers[intent.name][slot] = []
                if entity.is_builtin:
                    self.entity_parsers[intent.name][slot].append(
                        BUILTIN_ENTITY_ENTITY_PARSERS[entity.name]().fit(
                            dataset, slot, intent
                        )
                    )
                else:
                    for parser in self.entity_parsers_per_slot:
                        self.entity_parsers[intent.name][slot].append(
                            parser().fit(dataset, slot, intent)
                        )
        self.logger.debug(" Fit entity parsers...Done!")
        self.logger.debug("Fit...Done!")
        self.fitted = True
        return self

    @fitted_required
    def parse_utterance(
        self, utterance: str, threshold: float = 0.0
    ) -> IntentlyNLUResult | None:
        """Performs intent classification and slot filling on the provided `utterance`

        Args:
            utterance (str): The sentence/text to perform parsing on.
            threshold (float, optional): Parsing will fail if probability lower than this. Defaults to 0.0.

        Returns:
            IntentlyNLUResult | None: Result or `None` if no intent could be classified or
                                      slot filling for required slots failed.
        """
        self.logger = get_logger(__name__)
        self.logger.debug("Parse...")
        self.logger.debug(" Utterance: %s", utterance)
        intents: list[tuple[Intent, float]] = []
        self.logger.debug(" Classify...")
        for intent_classifier in self.intent_classifiers:
            intent = intent_classifier.classify(utterance)
            if intent is not None and intent[1] >= intent[0].matching_strictness:
                intents.append(intent)
                if intent[1] == 1:
                    break
        self.logger.debug(" Classify...Done!")
        if not intents:
            self.logger.debug(" No intent classified")
            self.logger.debug("Parse...Done!")
            return None
        intents.sort(key=lambda x: x[1], reverse=True)

        classified_intent = intents[0][0]
        score = intents[0][1]
        self.logger.debug(" Classified intent: %s", classified_intent)
        self.logger.debug(" Score: %s", score)

        self.logger.debug(" Resolve slots...")
        self.logger.debug("     Resolve required slots...")
        slots: dict[str, str] = {}
        for slot in classified_intent.required_slots:
            best_match: str | None = None
            best_score = 0.0
            for parser in self.entity_parsers[classified_intent.name][slot]:
                result = parser.parse(utterance)
                if result is not None and result[1] > best_score:
                    best_match = result[0]
                    best_score = result[1]
                    if best_score == 1:
                        break
            if (
                best_match is not None
                and best_score
                >= classified_intent.required_slots[slot].matching_strictness
            ):
                self.logger.debug("     Resolved %s for %s", best_match, slot)
                slots[slot] = best_match
            else:
                self.logger.debug("     Could not resolve %s", slot)
                self.logger.debug("     Resolve required slots...Done!")
                self.logger.debug(" Resolve slots...Done!")
                self.logger.debug("Parse...Done!")
                return None
        self.logger.debug("     Resolve optional slots...")
        for slot, entity in (
            classified_intent.optional_slots.items()
            if classified_intent.optional_slots
            else dict[str, Entity]().items()
        ):
            best_match_optional: str | None = None
            best_score_optional = 0.0
            for parser in self.entity_parsers[classified_intent.name][slot]:
                result = parser.parse(utterance)
                if result is not None and result[1] > best_score_optional:
                    best_match_optional = result[0]
                    best_score_optional = result[1]
                    if best_score_optional == 1:
                        break
            if (
                best_match_optional is not None
                and best_score_optional >= entity.matching_strictness
            ):
                self.logger.debug(
                    "     Resolved %s for optional %s", best_match_optional, slot
                )
                slots[slot] = best_match_optional
            else:
                self.logger.warning("     Could not resolve optional %s", slot)
        self.logger.debug("     Resolve optional slots...Done!")
        self.logger.debug(" Resolve slots...Done!")
        if score < threshold:
            self.logger.debug(" Score %s lower than threshold %s!", score, threshold)
            self.logger.debug("Parse...Done!")
            return None
        parsing_result = IntentlyNLUResult(
            utterance, classified_intent.name, score, slots
        )
        self.logger.debug(" Result: %s", parsing_result)
        self.logger.debug("Parse...Done!")
        return parsing_result

    @elapsed_time("Engine persisted in", warn_if_more_than=1)
    @fitted_required
    def persist(self, directory: str, filename: str) -> str:
        """Save the whole engine instance and its state in one file

        Args:
            directory (str): Where to store the file.
            filename (str): Name of the file. The actual name results in "`filename`.inlue`<model_version>`".

        Raises:
           FileNotFoundError: The specified directory does not exist

        Returns:
            str: Output path.
        """
        self.logger.debug("Persist engine...")
        self.logger.debug(" Directory: %s; name: %s", directory, filename)
        if not os.path.exists(directory):
            self.logger.error(
                "Cannot persist engine: The specified directory does not exist: %s",
                directory,
            )
            e = FileNotFoundError(
                f"Cannot persist engine: The specified directory does not exist: {directory}"
            )
            raise log_error(self.logger, e, "Persist engine") from e
        file_path = os.path.join(directory, filename + ".inlue" + __model_version__)
        self.logger.debug(" Path: %s", file_path)

        self.logger.debug(" Dump...")
        # Save the instance using dill
        with open(file_path, "wb") as f:
            dill.dump(self, f)  # type: ignore
        self.logger.debug(" Dump...Done!")
        self.logger.info("  Engine saved to %s", file_path)
        self.logger.debug("Persist engine...Done!")
        return file_path

    @classmethod
    @elapsed_time("Engine loaded in", warn_if_more_than=1)
    def from_file(
        cls: type["IntentlyNLUEngine"], directory: str, filename: str
    ) -> "IntentlyNLUEngine":
        """Load an instance of `IntentlyNLUEngine` from a file created earlier by `IntentlyNLUEngine.persist()`

        Args:
            directory (str): Where the file is stored.
            filename (str): Name of the engine.

        Raises:
            FileNotFoundError: If the file is not found.
            TypeError: If the file is not valid.

        Returns:
            IntentlyNLUEngine: The loaded instance if valid.
        """
        logger = get_logger(__name__)
        logger.debug("Recreate engine from file...")
        file_path = os.path.join(directory, filename + ".inlue" + __model_version__)
        logger.debug(" Path: %s", file_path)
        if not os.path.exists(file_path):
            e = FileNotFoundError(f"The specified file does not exist: {file_path}")
            raise log_error(logger, e, "Recreate engine from file") from e

        logger.debug("  Load engine...")
        with open(file_path, "rb") as f:
            loaded_instance = dill.load(f)  # type: ignore
        logger.debug("  Load engine...Done!")
        # Validate that the loaded object is an instance of IntentlyNLUEngine
        if not isinstance(loaded_instance, cls):
            e2 = TypeError(
                f"The loaded object ({type(loaded_instance)}) is not an instance of {cls.__name__}."
            )
            raise log_error(logger, e2, "Recreate engine from file") from e2

        logger.debug("Load engine from file...Done!")
        loaded_instance.logger.info("Engine was recreated from file.")
        return loaded_instance

    def __str__(self) -> str:
        return f"IntentlyNLUEngine({self.__dict__})"
