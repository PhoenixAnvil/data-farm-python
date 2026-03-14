from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Connection, Engine

from data_farm.l1_application.shared.helpers import optional_int, optional_query, optional_str, require_str
from data_farm.l2_interface_adapters.config.env import get_password_from_env, get_user_from_env


def build_conn_url(config: dict[str, Any]) -> URL:
    drivername = require_str(config, "driver")

    user_env = optional_str(config, "user_env")
    username = get_user_from_env(user_env)

    password_env = optional_str(config, "password_env")
    password = get_password_from_env(password_env)

    host = optional_str(config, "host")
    port = optional_int(config, "port")
    database = optional_str(config, "database")

    query = optional_query(config)

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
