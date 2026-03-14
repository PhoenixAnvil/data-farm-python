from __future__ import annotations

from pathlib import Path

from data_farm.l1_application.commands.inspect_command import InspectCommand
from data_farm.l1_application.context import AppContext
from data_farm.l1_application.inspect_workflow import (
    create_inspection_context,
    generate_data,
    get_generation_plans,
    inspect,
)


def run_inspect(app_ctx: AppContext, cmd: InspectCommand) -> int:
    insp_ctx = create_inspection_context(app_ctx, cmd)
    insp_res = inspect(app_ctx, insp_ctx.data_source_config, insp_ctx.schema)

    gen_plans = get_generation_plans(insp_ctx, insp_res)

    out_path = Path(cmd.output_file) if cmd.output_file else None

    generate_data(out_path, app_ctx, insp_ctx, insp_res, gen_plans)

    return 0
