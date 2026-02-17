from __future__ import annotations

from collections.abc import Iterable

from data_farm.emitters.base import Emitter
from data_farm.models.models import ColumnEmitDefinition
from data_farm.utils.enums import SqlType


class SqlEmitter(Emitter):
    """TBD"""

    def emit(self, table: str, emit_defs: list[ColumnEmitDefinition]) -> Iterable[str]:
        col_parts = []
        val_parts = []

        for ed in emit_defs:
            col_parts.append(ed.name)
            match ed.data_type:
                case SqlType.STRING:
                    out = f"'{ed.value}'"
                case SqlType.INTEGER:
                    out = f"{ed.value}"
                case SqlType.FLOAT:
                    out = f"{ed.value}"
                case SqlType.BOOLEAN:
                    out = f"{ed.value.lower()}"
                case SqlType.UUID:
                    out = f"'{ed.value}'"
                case SqlType.DATE:
                    out = f"{ed.value}"
                case SqlType.DATETIME:
                    out = f"{ed.value}"
                case SqlType.DECIMAL:
                    out = f"{ed.value}"
                case _:
                    out = ""
            val_parts.append(out)

        cols = ", ".join(col_parts)
        vals = ", ".join(val_parts)

        yield f"INSERT INTO {table} ({cols}) VALUES ({vals});"
