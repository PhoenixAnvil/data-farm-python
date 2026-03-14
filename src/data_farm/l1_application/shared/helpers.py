from collections.abc import Mapping
from typing import Any, cast


def require_str(config: dict[str, Any], key: str) -> str:
    value = config.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing or invalid '{key}' in config.")
    return value.strip()


def optional_str(config: dict[str, Any], key: str) -> str | None:
    value = config.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"Invalid '{key}' (expected string).")
    value = value.strip()
    return value or None


def optional_int(config: dict[str, Any], key: str) -> int | None:
    value = config.get(key)
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    raise ValueError(f"Invalid '{key}' (expected int).")


QueryMapping = Mapping[str, str]


def optional_query(config: dict[str, Any], key: str = "query") -> QueryMapping | None:
    raw = config.get(key)
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise ValueError(f"Invalid '{key}' (expected table/dict).")

    raw_dict = cast(dict[str, Any], raw)
    query: dict[str, str] = {}

    for k, v in raw_dict.items():
        if not isinstance(v, str | int | float | bool):
            raise ValueError(f"Invalid query param '{k}': must be simple scalar.")
        query[k] = str(v)

    return query
