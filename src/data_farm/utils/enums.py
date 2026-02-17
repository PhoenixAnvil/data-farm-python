from enum import StrEnum, auto


class SqlType(StrEnum):
    """Canonical dialect-agnostic SQL data types."""

    STRING = auto()
    FIXED_STRING = auto()
    TEXT = auto()
    INTEGER = auto()
    DECIMAL = auto()
    FLOAT = auto()
    DATETIME = auto()
    DATE = auto()
    TIME = auto()
    BOOLEAN = auto()
    UUID = auto()
    JSON = auto()
    BINARY = auto()
