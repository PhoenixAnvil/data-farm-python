from __future__ import annotations

from pathlib import Path

from data_farm.application.inspect_workflow import (
    create_inspection_context,
    generate_data,
    get_generation_plans,
    inspect,
)
from data_farm.cli.base import AppContext, InspectNamespace


def run_inspect(app_ctx: AppContext, ns: InspectNamespace) -> int:
    insp_ctx = create_inspection_context(app_ctx, ns)
    insp_res = inspect(insp_ctx.data_source_config, insp_ctx.schema)

    gen_plans = get_generation_plans(insp_ctx, insp_res)

    out_path = Path(ns.output_file) if ns.output_file else None

    generate_data(out_path, app_ctx, insp_ctx, insp_res, gen_plans)

    return 0
