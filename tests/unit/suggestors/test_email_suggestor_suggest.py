from collections.abc import Callable

import pytest

from data_farm.domain.model.models import ColumnInspection
from data_farm.domain.suggestors.builtins import EmailSuggestor

MakeCol = Callable[..., ColumnInspection]


@pytest.mark.parametrize(
    ("name"),
    ["email", "email1", "1email"],
    ids=["match-exact", "match-before", "match-after"],
)
def test_email_suggestor_returns_pattern_suggestion(make_col: MakeCol, name: str) -> None:
    # Arrange
    ci = make_col(name=name)
    CONFIDENCE = 0.9

    # Act
    suggestion = EmailSuggestor().suggest(ci)

    # Assert
    assert suggestion is not None
    assert suggestion.strategy == "email"
    assert suggestion.pattern_id == "email"
    assert suggestion.confidence >= CONFIDENCE
    assert "email" in suggestion.reason
    assert suggestion.suggestor == "email"
