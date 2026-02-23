# Data Farm (Python Edition)

Data Farm is a schema-aware test data generation tool designed for
engineers, QA professionals, and developers who need structured,
reproducible data for relational databases.

It inspects existing schemas, suggests generation strategies, and emits
SQL scripts using deterministic random generation.

------------------------------------------------------------------------

## Features

- Inspect relational database schemas
- Suggest generation strategies based on column types and patterns
- Deterministic random data generation (seed-based)
- SQL `INSERT` script emission
- CLI-first design
- Extensible architecture (planners, suggestors, emitters)
- Structured logging with UTC timestamps

------------------------------------------------------------------------

## Requirements

- Python 3.11+

------------------------------------------------------------------------

## Installation

Install from PyPI:

``` bash
pip install datafarm
```

After installation, the CLI command `dfarm` will be available.

------------------------------------------------------------------------

## Quick Start

### 1️⃣ Initialize a Project

Create a new Data Farm project:

``` bash
dfarm project init my_project
```

This creates a project directory containing configuration files.

------------------------------------------------------------------------

### 2️⃣ Configure the Project

Edit the generated configuration file (TOML format) to define:

- Database connection settings
- Target schema
- Generation options
- Output settings

------------------------------------------------------------------------

### 3️⃣ Inspect a Schema

Run schema inspection:

``` bash
dfarm inspect --config path/to/config.toml
```

Data Farm will:

- Connect to the configured data source
- Inspect tables and columns
- Suggest generation strategies
- Emit SQL scripts according to configuration

------------------------------------------------------------------------

## Example Workflow

``` bash
dfarm project init demo_project
# edit demo_project/config.toml

dfarm inspect --config demo_project/config.toml
```

Output SQL scripts can then be executed against your target database.

------------------------------------------------------------------------

## Logging

Data Farm uses structured logging with:

- UTC timestamps
- Verbosity levels (`-v`)
- Optional file logging (`--log-file`)

Example:

``` bash
dfarm inspect --config config.toml -v --log-file logs/
```

If a directory is provided to `--log-file`, a timestamped log file will
be created automatically.

------------------------------------------------------------------------

## CLI Overview

``` bash
dfarm --help
dfarm project --help
dfarm inspect --help
```

------------------------------------------------------------------------

## Architecture

Data Farm follows a layered design that separates:

- CLI interface
- Application orchestration
- Domain logic (suggestors, planners)
- Infrastructure (inspectors, emitters)

Future releases will further expand this architecture toward a full
DDD/Clean Architecture structure.

------------------------------------------------------------------------

## Development

Clone the repository:

``` bash
git clone https://github.com/PhoenixAnvil/data-farm-python.git
cd data-farm-python
```

Create a virtual environment:

``` bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

Install development dependencies:

``` bash
pip install -r requirements-dev.txt
```

Run tests:

``` bash
pytest
```

Build locally:

``` bash
python -m build
twine check dist/*
```

------------------------------------------------------------------------

## Contributing

Please see `CONTRIBUTING.md` for contribution guidelines.

All contributors are expected to follow the `CODE_OF_CONDUCT.md`.

------------------------------------------------------------------------

## License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

------------------------------------------------------------------------

## Roadmap

- v0.1.x --- Stabilization and packaging
- v0.2.0 --- DDD/Clean Architecture refactor
- v0.3.x --- Expanded planners and generation strategies

------------------------------------------------------------------------
