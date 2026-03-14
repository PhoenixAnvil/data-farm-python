""" """

import random
import string

from data_farm.field.text import TextFieldDefinition
from data_farm.l0_domain.generators.base import ValueGenerator


class TextGenerator(ValueGenerator):
    """Generate a value from a Pattern, respecting field constraints."""

    def __init__(
        self,
        rng: random.Random,
        choices: list[str],
        field_def: TextFieldDefinition,
    ) -> None:
        self.rng = rng
        self.choices = choices
        self.field_def = field_def

        min_len = field_def.min_length or 0
        max_len = field_def.max_length if field_def.max_length is not None else float("inf")

        # PERF: Precompute valid choices once; do not copy/mutate choices per row.
        self._valid_choices: list[str] = [c for c in choices if min_len <= len(c) <= max_len]

        if not self._valid_choices and not field_def.allow_null:
            # Fallback: generate a random string if no valid choices and field cannot be null
            self._valid_choices.append(
                "".join(rng.choices(string.ascii_letters + string.digits + string.punctuation, k=int(max_len)))
            )

    def generate(self) -> str | None:
        """Return a random valid choice, or None when nulls are allowed."""
        if not self._valid_choices:
            return None

        i = self.rng.randrange(len(self._valid_choices))
        return self._valid_choices[i]
