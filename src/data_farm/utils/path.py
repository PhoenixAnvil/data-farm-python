""" """

from pathlib import Path

from data_farm.messages.messages import msg


class FilePathValidator:
    def __init__(self, path: str | None = None):
        self.path = path

    def validate_path(self) -> Path:
        """TBD"""
        if self.path is None:
            raise ValueError(msg("err.utils.path.no_src"))

        path = Path(self.path)

        if not path.exists():
            raise FileNotFoundError(msg("err.utils.path.no_exist", path=path))

        if not path.is_file():
            raise ValueError(msg("err.utils.path.not_file", path=path))

        return path
