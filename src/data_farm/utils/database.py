from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any, cast

from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Connection, Engine


def build_conn_url(config: dict[str, Any]) -> URL:
    drivername = _require_str(config, "driver")

    user_env = _optional_str(config, "user_env")
    username = get_user_from_env(user_env)

    password_env = _optional_str(config, "password_env")
    password = get_password_from_env(password_env)

    host = _optional_str(config, "host")
    port = _optional_int(config, "port")
    database = _optional_str(config, "database")

    query = _optional_query(config)

    kwargs: dict[str, Any] = {
        "drivername": drivername,
        "username": username,
        "password": password,
        "host": host,
        "port": port,
        "database": database,
    }

    if query is not None:
        kwargs["query"] = query

    return URL.create(**kwargs)


def get_user_from_env(username_env: str | None):
    if username_env is not None:
        username = os.environ.get(username_env)
        if not username:
            raise ValueError(f"Could not read username from environment {username_env}.")
        else:
            return username
    else:
        raise ValueError("username_env=None")


def get_password_from_env(password_env: str | None):
    if password_env is not None:
        password = os.environ.get(password_env)
        if not password:
            raise ValueError(f"Could not read password from environment {password_env}.")
        else:
            return password
    else:
        raise ValueError("password_env=None")


def create_db_engine(config: dict[str, Any]) -> Engine:
    """
    Create a SQLAlchemy Engine (connection pool owner).

    We intentionally create the Engine once and reuse it, rather than
    creating a new Engine on every connect call.
    """
    conn_url = build_conn_url(config)
    echo = bool(config.get("echo", False))
    return create_engine(conn_url, echo=echo)


def connect(engine: Engine) -> Connection:
    """Open and return a Connection from an Engine."""
    return engine.connect()


def disconnect(conn: Connection) -> None:
    """Close a Connection."""
    conn.close()


def dispose_engine(engine: Engine) -> None:
    """
    Dispose the Engine's connection pool.

    This closes pooled connections and releases DB handles.
    """
    engine.dispose()


def _require_str(config: dict[str, Any], key: str) -> str:
    value = config.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing or invalid '{key}' in config.")
    return value.strip()


def _optional_str(config: dict[str, Any], key: str) -> str | None:
    value = config.get(key)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"Invalid '{key}' (expected string).")
    value = value.strip()
    return value or None


def _optional_int(config: dict[str, Any], key: str) -> int | None:
    value = config.get(key)
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    raise ValueError(f"Invalid '{key}' (expected int).")


QueryMapping = Mapping[str, str]


def _optional_query(config: dict[str, Any], key: str = "query") -> QueryMapping | None:
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
