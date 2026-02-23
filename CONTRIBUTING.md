# Contributing to Data Farm (Python Edition)

Thanks for your interest in **Data Farm**! 🎉\
Data Farm is a schema-aware test data generation tool for databases,
CSV, JSON, and other structured sources.

------------------------------------------------------------------------

## Quick Links

- Repo: <https://github.com/PhoenixAnvil/data-farm-python>
- Issues: <https://github.com/PhoenixAnvil/data-farm-python/issues>
- Project Board:
    <https://github.com/users/PhoenixAnvil/projects/1/views/1>

------------------------------------------------------------------------

## Code of Conduct

This project follows the Contributor Covenant Code of Conduct. By
participating, you agree to uphold it.

Please see `CODE_OF_CONDUCT.md` for reporting instructions.

------------------------------------------------------------------------

## What to Work On

### Good First Contributions

- Documentation improvements (README, docs, examples)
- Tests that lock in behavior (especially edge cases + invariants)
- Small bug fixes or refactors that reduce complexity
- New planner/suggestor coverage for missing SQL/data types

### How Work Is Tracked

- Issues are the source of truth for bugs and features
- The Project board tracks status and progress

If unsure what to pick up, comment on an issue:

> "I'd like to take this one. Any gotchas before I start?"

------------------------------------------------------------------------

## Filing Issues

### Bug Reports

Include:

- Expected vs actual behavior
- CLI command used (redact secrets)
- OS + Python version
- Minimal reproduction steps
- Relevant logs or stack traces

### Feature Requests

Include:

- The problem you're solving (the "why")
- Proposed CLI shape (example command/output)
- Constraints (performance, determinism, compatibility)

------------------------------------------------------------------------

## Development Setup

### Prerequisites

- Python 3.11+
- git
- Optional: make

### Clone

``` bash
git clone https://github.com/PhoenixAnvil/data-farm-python.git
cd data-farm-python
```

### Virtual Environment

``` bash
python -m venv .venv
# Windows PowerShell:
. .\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
```

### Install Dev Dependencies

``` bash
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

------------------------------------------------------------------------

## Tooling & Quality Gates

### Install Pre-commit Hooks

``` bash
pre-commit install
```

### Run All Hooks

``` bash
pre-commit run --all-files
```

### Formatting (Black)

``` bash
black .
```

### Linting (Ruff)

``` bash
ruff check . --fix
```

### Tests (pytest)

``` bash
pytest
```

------------------------------------------------------------------------

## Running Data Farm Locally

After editable install:

``` bash
dfarm --help
```

If contributing new commands or flags, include examples in docs or
examples folder.

------------------------------------------------------------------------

## Branches, Commits, PRs

### Branch Naming

- bugfix/`<short-description>`{=html}
- feature/`<short-description>`{=html}
- docs/`<short-description>`{=html}
- test/`<short-description>`{=html}
- refactor/`<short-description>`{=html}

Example:

- feature/planner-uuid

### Commits

- One logical change per commit
- Clear message explaining why
- Keep diffs focused and reviewable

### PR Checklist

Before opening a PR:

- [ ] Tests added or updated
- [ ] pytest passes locally
- [ ] pre-commit passes
- [ ] Docs updated if behavior changed
- [ ] No secrets committed

In PR description include:

- What changed and why
- Link to issue (e.g. Closes #123)
- Design notes or tradeoffs

------------------------------------------------------------------------

## Design Expectations

Data Farm aims to be:

- Deterministic (seeded output)
- CLI-friendly (clear messages, helpful errors)
- Testable (thin CLI boundary, logic in classes/functions)
- Readable (clarity over cleverness)

When adding generators/planners/suggestors:

- Add invariant-based tests
- Include at least one realistic example
- Consider performance (avoid heavy per-row logic)

------------------------------------------------------------------------

## Security

If you discover a security issue, do not open a public issue. Follow
contact instructions in CODE_OF_CONDUCT.md.

------------------------------------------------------------------------

## License

By contributing, you agree that your contributions are licensed under
the MIT License.
