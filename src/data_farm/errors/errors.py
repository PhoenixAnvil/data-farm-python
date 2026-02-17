"""

"""


class DataFarmError(Exception):
    """Base exception for Data Farm."""
    pass


class EmptyInputFileError(DataFarmError):
    """Raised when an input file contains no usable data."""
    pass
