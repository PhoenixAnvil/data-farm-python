""" """

from pathlib import Path

from data_farm.messages.messages import msg


class FilePathValidator:
    def __init__(self, path: Path | None = None):
        self.path = path

    def validate_path(self) -> Path:
        """TBD"""
        if self.path is None:
            raise ValueError(msg("err.utils.path.no_src"))

        if not self.path.exists():
            raise FileNotFoundError(msg("err.utils.path.no_exist", path=self.path))

        if not self.path.is_file():
            raise ValueError(msg("err.utils.path.not_file", path=self.path))

        return self.path
