from __future__ import annotations

from typing import Any

from sqlalchemy import MetaData, Table, func, inspect, select, text
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.engine.interfaces import ReflectedColumn
from sqlalchemy.engine.reflection import Inspector as SAInspector

from data_farm.l0_domain.enums import SqlType
from data_farm.l0_domain.model.models import ColumnInspection, NormalizedColumnType, TableInspection
from data_farm.l1_application.ports.inspector import Inspector
from data_farm.l2_interface_adapters.database.database import connect, create_db_engine, disconnect, dispose_engine
from data_farm.messages.messages import msg


class DatabaseInspector(Inspector):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__(config)
        self.engine: Engine | None = None
        self.conn: Connection | None = None
        self.err_no_conn: str = "err.dbinspector.not_conn"

    def connect(self) -> None:
        try:
            if self.engine is None:
                self.engine = create_db_engine(self.config)
            if self.conn is None:
                self.conn = connect(self.engine)
        except Exception:
            self.disconnect()
            raise

    def disconnect(self) -> None:
        if self.conn is not None:
            disconnect(self.conn)
            self.conn = None

        if self.engine is not None:
            dispose_engine(self.engine)
            self.engine = None

    def query(self, expression: str) -> list[dict[str, Any]]:
        if self.conn is None:
            raise RuntimeError(msg(self.err_no_conn))

        result = self.conn.execute(text(expression))
        # Convert RowMapping -> plain dict (keeps SQLAlchemy out of downstream code)
        return [dict(row) for row in result.mappings().all()]

    def row_count(self, count_table: str, schema: str | None = None) -> int:
        if self.conn is None:
            raise RuntimeError(msg(self.err_no_conn))

        metadata = MetaData()

        t = Table(
            count_table,
            metadata,
            autoload_with=self.engine,
            schema=schema,
        )

        stmt = select(func.count()).select_from(t)
        return int(self.conn.execute(stmt).scalar_one())

    def inspect_table(self, table: str, *, schema: str | None = None) -> TableInspection:
        """
        Inspect a table's columns' metadata.
        """
        col_meta = self._get_columns(table, schema=schema)
        rows = self.row_count(table, schema) if schema else self.row_count(table)

        return TableInspection(
            table=table,
            schema=schema,
            columns=col_meta,
            row_count=rows,
        )

    def inspect_many_tables(self, tables: list[str], schema: str | None = None) -> list[TableInspection]:
        all_tables = self._get_tables(schema=schema)
        for tbl in tables:
            if tbl not in all_tables:
                raise ValueError(msg("err.dbinspector.tbl_no_exist", table=tbl))

        return [self.inspect_table(t, schema=schema) for t in tables]

    def inspect_all_tables(self, schema: str | None = None) -> list[TableInspection]:
        all_tables = self._get_tables(schema)
        return [self.inspect_table(t, schema=schema) for t in all_tables]

    def _require_conn(self) -> Connection:
        if self.conn is None:
            raise RuntimeError(msg(self.err_no_conn))
        return self.conn

    def _sa_inspector(self) -> SAInspector:
        return inspect(self._require_conn())

    def _get_schemas(self) -> list[str]:
        insp = self._sa_inspector()
        return insp.get_schema_names()

    def _get_tables(self, schema: str | None = None) -> list[str]:
        insp = self._sa_inspector()
        return insp.get_table_names(schema=schema)

    def _get_columns(self, table: str, schema: str | None = None) -> list[ColumnInspection]:
        """
        Returns SQLAlchemy-reflected column info as domain objects.

        Typical keys include: name, type, nullable, default, autoincrement, comment...
        Exact keys vary slightly by dialect.
        """
        insp = self._sa_inspector()
        cols: list[ReflectedColumn] = insp.get_columns(table_name=table, schema=schema)

        # Ensure everything is JSON-ish / plain Python.
        # "type" is often a SQLAlchemy TypeEngine, so stringify it.
        cleaned: list[ColumnInspection] = []
        for c in cols:
            # Normalize the "easy to vary" fields defensively.
            name_raw = c.get("name")
            type_raw = c.get("type")
            nullable_raw = c.get("nullable")

            if not name_raw:
                raise ValueError(f"Inspector returned invalid column name: {name_raw!r}")

            cleaned.append(
                ColumnInspection(
                    table=table,
                    name=name_raw,
                    data_type=self._normalize_type(str(type_raw)),
                    nullable=bool(nullable_raw),
                    length=None,
                    default=c.get("default"),
                    autoincrement=(
                        c.get("autoincrement")
                        if isinstance(c.get("autoincrement"), bool) or c.get("autoincrement") is None
                        else bool(c.get("autoincrement"))
                    ),
                    comment=(
                        c.get("comment")
                        if isinstance(c.get("comment"), str) or c.get("comment") is None
                        else str(c.get("comment"))
                    ),
                    is_primary_key=False,
                    is_foreign_key=False,
                    foreign_key=None,
                )
            )

        return cleaned

    def _get_primary_key(self, table: str, schema: str | None = None) -> list[str]:
        insp = self._sa_inspector()
        pk = insp.get_pk_constraint(table_name=table, schema=schema)
        cols = pk.get("constrained_columns") or []
        return list(cols)

    def _get_foreign_keys(self, table: str, schema: str | None = None) -> list[dict[str, Any]]:
        insp = self._sa_inspector()
        fks = insp.get_foreign_keys(table_name=table, schema=schema)

        cleaned: list[dict[str, Any]] = []
        for fk in fks:
            cleaned.append(
                {
                    "name": fk.get("name"),
                    "constrained_columns": fk.get("constrained_columns") or [],
                    "referred_schema": fk.get("referred_schema"),
                    "referred_table": fk.get("referred_table"),
                    "referred_columns": fk.get("referred_columns") or [],
                    "options": fk.get("options") or {},
                }
            )
        return cleaned

    def _normalize_type(self, type_raw: str) -> NormalizedColumnType:
        """Normalize SQL data types into domain type."""

        name: SqlType | None = None
        params: list[int] | None = None

        if not type_raw.strip():
            raise ValueError(f"Cannot normalize type {type_raw}.")
        name = self._get_type_name(type_raw)
        if not name:
            raise ValueError(f"Cannot normalize type {type_raw}.")
        params = self._get_type_params(type_raw)

        return self.normalize_params(params, name)

    def normalize_params(self, params: list[int] | None, name: SqlType) -> NormalizedColumnType:
        length = None
        num_precision = None
        scale = None
        time_precision = None

        PRECISION_AND_SCALE = 2

        if not params:
            return NormalizedColumnType(name, None, None, None, None)
        if len(params) == 1 and name in (SqlType.STRING, SqlType.FIXED_STRING):
            length = params[0]
        elif len(params) == 1 and name in (SqlType.DECIMAL):
            num_precision = params[0]
        elif len(params) == PRECISION_AND_SCALE and name in (SqlType.DECIMAL):
            num_precision = params[0]
            scale = params[1]
        elif len(params) == 1 and name == SqlType.DATETIME:
            time_precision = params[0]
        return NormalizedColumnType(name, length, num_precision, scale, time_precision)

    def _normalize_type_name(self, name: str) -> SqlType | None:
        """TBD"""

        name = name.strip().upper()

        if not name:
            return None

        if name.startswith("TEXT"):
            return SqlType.TEXT
        elif name.startswith(("VARCHAR", "CHARACTER VARYING")):
            return SqlType.STRING
        elif name.startswith(("CHAR", "CHARACTER", "BPCHAR")):
            return SqlType.FIXED_STRING
        elif name.startswith(("SMALLINT", "INTEGER", "BIGINT")):
            return SqlType.INTEGER
        elif name.startswith(("NUMERIC", "DECIMAL")):
            return SqlType.DECIMAL
        elif name.startswith("TIMESTAMP"):
            return SqlType.DATETIME
        elif name.startswith("BOOLEAN"):
            return SqlType.BOOLEAN
        elif name.startswith("UUID"):
            return SqlType.UUID
        elif name.startswith("JSON"):
            return SqlType.JSON

    def _has_params(self, type_name: str) -> bool:
        """
        Determine if a raw type has any parameters.

        If a type has one or more parameters, a (
        character normally delineates the parameter
        list.
        """

        return "(" in type_name

    def _get_type_name(self, raw_name: str) -> SqlType | None:
        if self._has_params(raw_name):
            name = raw_name.split("(", maxsplit=1)[0]
            parsed_name = self._parse_type_name(name)
            if parsed_name is None:
                return None
            return self._normalize_type_name(parsed_name)
        parsed_name = self._parse_type_name(raw_name)
        if parsed_name is None:
            return None
        return self._normalize_type_name(parsed_name)

    def _get_type_params(self, raw_type: str) -> list[int] | None:
        if self._has_params(raw_type):
            params = raw_type.split("(", maxsplit=1)[1]
            if not params:
                return None
            if params[-1] != ")":
                raise ValueError(f"Cannot parse params {params} for raw type {raw_type}.")
            return self._parse_type_params(params)
        return None

    def _parse_type_name(self, name: str) -> str | None:
        parsed_name = name.strip()
        if not parsed_name:
            return None
        parsed_name = parsed_name.upper()
        return parsed_name

    def _parse_type_params(self, params: str) -> list[int] | None:
        parsed_params = params.strip().rstrip(")")
        if not parsed_params:
            return None
        param_list = []
        if "," in parsed_params:
            param_list = parsed_params.split(",", maxsplit=1)
            param_list[0] = param_list[0].strip()
            param_list[1] = param_list[1].strip()
            if not param_list[0].isdigit() or not param_list[1].isdigit():
                return None
        if parsed_params.isdigit():
            param_list.append(parsed_params)
        return [int(p) for p in param_list if p.strip() and p.isdigit()] or None

    def _has_math_symbols(self, text: str) -> bool:
        math_symbols = ["+", "-", "/", "*"]
        return any(ms in text for ms in math_symbols)
