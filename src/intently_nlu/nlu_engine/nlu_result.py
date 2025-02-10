"""Represents the result of an `IntentlyNLUEngine`"""

from dataclasses import dataclass


@dataclass(frozen=True)
class IntentlyNLUResult:
    """Represents the result of an `IntentlyNLUEngine`"""

    raw_utterance: str
    intent: str
    probability: float
    resolved_slots: dict[str, str]
