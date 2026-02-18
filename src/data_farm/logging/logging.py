from datetime import datetime, timezone


def generate_log_file_name() -> str:
    """Generate a name for the Data Farm log file."""
    return f"data_farm_{datetime.now(timezone.utc):%Y%m%d_%H%M%S}.log"
