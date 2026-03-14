from pathlib import Path

from data_farm.l1_application.commands.inspect_command import InspectCommand
from data_farm.l3_frameworks_and_drivers.cli.base import InspectNamespace


def to_inspect_command(ns: InspectNamespace) -> InspectCommand:
    return InspectCommand(
        project=Path(ns.project),
        rows=ns.rows,
        schema=ns.schema,
        insert_batch_size=ns.insert_batch_size,
        output_file=ns.output_file,
    )
