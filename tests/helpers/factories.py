from collections.abc import Callable

import pytest

from data_farm.models.models import ColumnInspection, NormalizedColumnType
from data_farm.utils.enums import SqlType


@pytest.fixture
def make_col() -> Callable[..., ColumnInspection]:
    def _make(
        *,
        name: str,
        sql_type: SqlType = SqlType.STRING,
        length: int | None = 50,
        table: str = "qa",
    ) -> ColumnInspection:
        return ColumnInspection(
            table=table,
            name=name,
            data_type=NormalizedColumnType(sql_type, length, None, None, None),
            nullable=True,
            is_primary_key=False,
            is_foreign_key=False,
            comment=None,
        )

    return _make
