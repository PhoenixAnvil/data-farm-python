from __future__ import annotations

from data_farm.l0_domain.enums import SqlType
from data_farm.l0_domain.model.models import ColumnInspection, NormalizedColumnType
from data_farm.l0_domain.suggestors.builtins import (
    StatusCodeSuggestor,
    TimestampSuggestor,
    UuidSuggestor,
)
from data_farm.l0_domain.suggestors.defaults import build_default_registry
from data_farm.l0_domain.suggestors.engine import suggest_for_column


def test_uuid_suggestor_by_name_suffix() -> None:
    CONF = 0.90
    col = ColumnInspection(
        table="t1",
        name="order_uuid",
        data_type=NormalizedColumnType(SqlType.STRING, 36, None, None, None),
        nullable=False,
    )
    s = UuidSuggestor().suggest(col)
    assert s is not None
    assert s.strategy == "uuid"
    assert s.pattern_id == "uuid"
    assert s.confidence >= CONF


def test_timestamp_suggestor_prefers_type_when_datetimeish() -> None:
    CONF = 0.70
    col = ColumnInspection(
        table="t1",
        name="created_at",
        data_type=NormalizedColumnType(SqlType.DATETIME, None, None, None, None),
        nullable=False,
    )
    s = TimestampSuggestor().suggest(col)
    assert s is not None
    assert s.strategy.startswith("datetime")
    assert s.pattern_id == "datetime_recent"
    assert s.confidence >= CONF


def test_status_code_suggestor_only_for_stringy_types() -> None:
    col = ColumnInspection(
        table="t1",
        name="status_code",
        data_type=NormalizedColumnType(SqlType.STRING, 16, None, None, None),
        nullable=False,
    )
    s = StatusCodeSuggestor().suggest(col)
    assert s is not None
    assert s.strategy == "choice_pool"
    assert s.pattern_id == "choice_pool"


def test_foreign_key_suggestor_beats_name_based_on_priority() -> None:
    # ForeignKeySuggestor has high priority and should win even if name matches another suggestor.
    CONF = 0.95
    col = ColumnInspection(
        table="t1",
        name="email",
        data_type=NormalizedColumnType(SqlType.STRING, 64, None, None, None),
        nullable=False,
        is_foreign_key=True,
        foreign_key={"referred_table": "users"},
    )

    # Manually supply a list where email suggestor might also match.

    reg = build_default_registry()
    best = suggest_for_column(col, reg.all())

    assert best.strategy == "fk_reference"
    assert best.confidence >= CONF
    assert "foreign key" in best.reason.lower()
