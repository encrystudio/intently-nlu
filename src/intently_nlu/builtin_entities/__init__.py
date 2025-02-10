"""Builtin entity initialization"""

from .number import NumberEntityParser, get_number_entity

BUILTIN_ENTITY_ENTITY_PARSERS = {"intently/entities/number": NumberEntityParser}

BUILTIN_ENTITIES = {"intently/entities/number": get_number_entity}
