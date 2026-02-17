""" """

import random

from data_farm.field.text import TextFieldDefinition
from data_farm.generators.base import ValueGenerator
from data_farm.patterns.base import Pattern


class TextGenerator(ValueGenerator):
    """TBD"""

    def __init__(
        self,
        rng: random.Random,
        pattern: Pattern,
        field_def: TextFieldDefinition,
    ):
        self.rng = rng
        self.pattern = pattern
        self.field_def = field_def

    def generate(self) -> str | None:
        """TBD"""
        msg1 = "Valid choice cannot be found"
        msg2 = " and field cannot be null."
        error_message = f"{msg1}{msg2}"
        choices = self.pattern.choices.copy()

        if not self.__is_sane(choices):
            raise ValueError(error_message)

        choice = self.__get_choice(choices)
        if choice is None and not self.field_def.allow_null:
            raise ValueError(error_message)

        return choice

    def __is_sane(self, choices: list[str]) -> bool:
        return bool(choices) or self.field_def.allow_null

    def __get_choice(self, choices: list[str]) -> str | None:
        while choices:
            i = self.rng.randrange(len(choices))
            choice = choices[i]

            if self.__is_valid(choice):
                return choice

            choices[i] = choices[-1]
            choices.pop()

        return None

    def __is_valid(self, choice: str) -> bool:
        min_len = self.field_def.min_length or 0
        max_len = self.field_def.max_length or float("inf")
        return min_len <= len(choice) <= max_len
