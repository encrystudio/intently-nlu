"""Intent classifier initialization"""

from .deterministic_intent_classifier import DeterministicIntentClassifier
from .fuzzy_intent_classifier import FuzzyIntentClassifier
from .intent_classifier import IntentClassifier

BUILTIN_INTENT_CLASSIFIERS: dict[str, type[IntentClassifier]] = {
    "DeterministicIntentClassifier": DeterministicIntentClassifier,
    "FuzzyIntentClassifier": FuzzyIntentClassifier,
}
