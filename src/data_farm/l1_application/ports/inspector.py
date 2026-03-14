from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any


class Inspector(ABC):
    """TBD"""

    def __init__(self, config: dict[str, Any]):
        """Initialize a new Inspector object with a valid config."""
        self.config = config

    def __enter__(self) -> "Inspector":
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        # Always clean up. Returning None means "do not suppress exceptions".
        self.disconnect()

    @abstractmethod
    def connect(self):
        """Connect to a database or open a file."""
        pass

    @abstractmethod
    def query(self, expression: str) -> list[dict[str, Any]]:
        """
        Query the underlying data source.
        """
        pass

    @abstractmethod
    def row_count(self, count_table: str) -> int:
        """
        Return a count of rows in the specified table.
        """
        ...

    @abstractmethod
    def disconnect(self):
        """Disconnect from a database or close a file."""
        pass
