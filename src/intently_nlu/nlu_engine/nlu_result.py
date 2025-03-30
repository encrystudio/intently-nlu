"""Represents the result of an `IntentlyNLUEngine`"""

from dataclasses import dataclass


@dataclass(frozen=True)
class IntentlyNLUResult:
    """Represents the result of an `IntentlyNLUEngine`"""

    raw_utterance: str
    intent: str
    probability: float
    resolved_slots: dict[str, str]

    def as_json(self) -> str:
        from intently_nlu.util.representation import json_string

        return json_string(self.__dict__)
