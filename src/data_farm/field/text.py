""" """

import random

from data_farm.field.base import FieldDefinition
from data_farm.messages.messages import msg
from data_farm.utils.random import random_int


class TextFieldDefinition(FieldDefinition):
    """TBD"""

    def __init__(
        self,
        allow_null: bool = False,
        fixed_length: int | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
    ):
        """TBD"""
        super().__init__(allow_null=allow_null)
        self.fixed_length = fixed_length
        self.min_length = min_length
        self.max_length = max_length

    def length(self, rng: random.Random) -> int:
        """TBD"""
        if self.fixed_length is not None:
            return self.fixed_length

        if self.min_length is None or self.max_length is None:
            raise ValueError(msg("err.text_field_def.min_max_required"))

        return random_int(rng, self.min_length, self.max_length)
