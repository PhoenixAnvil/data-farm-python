""" """

from data_farm.errors.errors import EmptyInputFileError
from data_farm.utils.path import FilePathValidator


class Pattern:
    """TBD"""

    def __init__(self, classification: str, choices: list[str] | None = None, source_path: str | None = None):
        """TBD"""
        self.classification = classification
        self.choices = choices or []
        self.source_path = source_path

    def load_from_file(self, clear: bool = True, encoding: str = "utf-8") -> None:
        """TBD"""
        source_path_is_empty = f"Input file is empty: {self.source_path}."

        path_val = FilePathValidator()
        path_val.path = self.source_path
        path = path_val.validate_path()

        with path.open("r", encoding=encoding) as f:
            self.classification = f.readline()
            lines = f.readlines()

        if not lines:
            raise EmptyInputFileError(source_path_is_empty)

        if clear:
            self.choices.clear()

        for line in lines:
            value = line.strip()
            if value:
                self.choices.append(value)
