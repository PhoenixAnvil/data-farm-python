# Data Farm (Python Edition)

Data Farm is a schema-aware test data generation tool for databases, CSV files, JSON files, and other structured data formats.

## Version

The current release is **`v0.1.0`**.

## Features

Data Farm can:

- Infer appropriate data types and generation strategies from existing schemas.
- Generate data using user-defined *field definitions* that control how values are produced.
- Generate data using user-defined *pattern definitions*, which provide reusable pools of valid values for selection.
- Generate data as **`.sql`** script files or insert it directly into a database or source file.
- Store target data source connection details in **`.toml`** configuration files.
- Generate data that validates specific field characteristics, such as minimum and maximum length, numeric-only, alphabetic-only, special-character-only, or defined combinations of character classes.

## Philosophy

Data Farm is designed to support realistic, repeatable, and configurable test data generation for QA and development workflows.

## Non-Goals

- Data Farm is not intended to replace full ETL pipelines.
- Data Farm does not attempt to generate production-grade synthetic data.

## License

This project is licensed under the [MIT License](https://mit-license.org/).  
See the LICENSE file in the root of this repository for details.
