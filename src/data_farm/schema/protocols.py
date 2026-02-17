# data_farm/schema/protocols.py (or schema/types.py)
from __future__ import annotations

from typing import Protocol

from data_farm.models.models import TableInspection


class RelationalInspector(Protocol):
    def inspect_table(self, table: str, schema: str | None = None) -> TableInspection: ...

    def inspect_many_tables(self, tables: list[str], schema: str | None = None) -> list[TableInspection]: ...
    def inspect_all_tables(self, schema: str | None = None) -> list[TableInspection]: ...
