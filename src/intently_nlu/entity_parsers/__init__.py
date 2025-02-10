"""Entity parser initialization"""

from .crf_entity_parser import CRFEntityParser
from .deterministic_entity_parser import DeterministicEntityParser
from .entity_parser import EntityParser

BUILTIN_ENTITY_PARSERS: dict[str, type[EntityParser]] = {
    "DeterministicEntityParser": DeterministicEntityParser,
    "CRFEntityParser": CRFEntityParser,
}
