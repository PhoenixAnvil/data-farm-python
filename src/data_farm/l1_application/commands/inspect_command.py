from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InspectCommand:
    project: Path
    schema: str
    insert_batch_size: int
    rows: int | None = None
    output_file: str | None = None
    # add whatever else you currently read from InspectNamespace
    # e.g. tables: tuple[str, ...] | None = None
    # config: Path | None = None
