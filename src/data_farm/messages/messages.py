from typing import Final

MESSAGES: Final[dict[str, str]] = {
    # Errors
    "err.planner.not_found": "Planner could not be found for column {column} of type {sql_type} in table {table} and strategy {strategy}.",
    "err.text_field_def.min_max_required": "min_length and max_length are required when fixed_length is not set.",
    "err.planner.numeric.precision": "precision must be > 0",
    "err.planner.numeric.scale": "scale must be between 0 and precision",
    "err.planner.empty_strategy": "Planner strategy/alias cannot be empty.",
    "err.planner.already.registered": "Planner already registered for strategy '{planner}'.",
    "err.dbinspector.not_conn": "DatabaseInspector is not connected.",
    "err.dbinspector.tbl_no_exist": "Table {table} does not exist in the database.",
    "err.utils.config.val_data_src_cfg": "Config not valid.",
    "err.utils.config.dir_create_fail": "Could not create data dir for data farm: {path}.",
    "err.utils.path.no_src": "Source path not provided.",
    "err.utils.path.no_exist": "Source path does not exist: {path}.",
    "err.utils.path.not_file": "Source path is not a file: {path}.",
    "err.utils.path.not_dir": "Source path is not a directory: {path}.",
    # CLI Help
    "cli.help.global.debug": "Enable debugging",
    "cli.help.global.verbose": "Increase verbosity (-v = INFO, -vv = DEBUG)",
    "cli.help.global.log_file": "Write logs to file (in addition to stderr)",
    "cli.help.app": "Override app config",
    "cli.help.app.ovr_cfg_dir": "Override default app config directory",
    "cli.help.app.ovr_data_dir": "Override default data directory",
    "cli.help.app.ovr_cfg_path": "Override default config file path",
    "cli.help.prj.manage": "Manage Data Farm projects",
    "cli.help.prj.set_root": "Set the root directory containing Data Farm projects",
    "cli.help.prj.init": "Initialize a new Data Farm project",
    "cli.help.prj.list": "List all Data Farm projects in projects root directory",
    "cli.help.insp": "Inspect a data source",
    "cli.help.insp.project": "Data Farm project name or path",
    "cli.help.insp.config": "Data source config path",
    "cli.help.insp.seed": "Seed value for the random number generator",
    "cli.help.insp.table": "The database table to generate data for",
    "cli.help.insp.rows": "Number of rows to generate per table",
    "cli.help.insp.out": "Emit INSERT statements to file",
    "cli.help.rng": "Manage the random number generator",
    "cli.help.rng.seed": "Provide a seed value for the random number generator",
}


def msg(key: str, **kwargs: object) -> str:
    try:
        template = MESSAGES[key]
    except KeyError as e:
        raise KeyError(f"Missing message key: {key}") from e
    return template.format(**kwargs)
