from __future__ import annotations

import random

from data_farm.field.text import TextFieldDefinition
from data_farm.generators.text import TextGenerator
from data_farm.patterns.base import Pattern


def test_text_generator_filters_choices_by_length() -> None:
    rng = random.Random(1)
    pat = Pattern(classification="x", choices=["a", "abcd", "abcdef", "zz"])
    field = TextFieldDefinition(allow_null=False, fixed_length=None, min_length=2, max_length=4)
    gen = TextGenerator(rng, pat, field)

    # Valid choices should be only "abcd" and "zz"
    values = {gen.generate() for _ in range(10)}
    assert values.issubset({"abcd", "zz"})


def test_text_generator_falls_back_when_no_valid_and_not_nullable() -> None:
    rng = random.Random(1)
    pat = Pattern(classification="x", choices=["a", "b"])
    field = TextFieldDefinition(allow_null=False, fixed_length=None, min_length=3, max_length=4)
    value = TextGenerator(rng, pat, field).generate()
    assert value is not None
    assert "m<*x" in value


def test_text_generator_returns_none_when_no_valid_and_nullable() -> None:
    rng = random.Random(1)
    pat = Pattern(classification="x", choices=["a", "b"])
    field = TextFieldDefinition(allow_null=True, fixed_length=None, min_length=3, max_length=4)
    gen = TextGenerator(rng, pat, field)
    assert gen.generate() is None
