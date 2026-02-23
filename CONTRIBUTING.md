# Contributing to Data Farm (Python Edition)

Thanks for your interest in contributing to **Data Farm**! 🎉  
Data Farm is a schema-aware test-data generation tool for databases, CSV, JSON, and other structured sources.

This guide covers how to:

- Propose ideas / ask questions
- File issues and bug reports
- Set up a local dev environment
- Submit high-quality pull requests

---

## Quick links

- Repo: [GitHub](https://github.com/PhoenixAnvil/data-farm-python)
- Issues: [GitHub Issues](https://github.com/PhoenixAnvil/data-farm-python/issues)
- Project Board: [GitHub Project](https://github.com/users/PhoenixAnvil/projects/1/views/1)

---

## Code of Conduct

This project follows the **Contributor Covenant Code of Conduct**.

By participating, you agree to uphold it. Please see `CODE_OF_CONDUCT.md` for details and reporting instructions.

---

## What to work on

### Good first contributions

- Documentation improvements (README, docs, examples)
- Tests that lock in behavior (edge cases + invariants)
- Small bug fixes or refactors that reduce complexity
- New planner/suggestor coverage for missing SQL/data types (when tracked in Issues)

### How work is tracked

- **Issues** are the source of truth for bugs/features
- The **Project Board** tracks status/progress across issues and PRs

If you’re unsure what to pick up, grab an issue and leave a short comment like:

> I’d like to take this one. Any gotchas before I start?

---

## Filing issues (bugs, features, questions)

### Bug reports

Please include:

- What you expected vs what happened
- The CLI command you ran (redact secrets)
- OS + Python version
- Minimal reproduction steps
- Relevant logs / stack traces

### Feature requests

Please include:

- The problem you’re solving (the “why”)
- A proposed UX/CLI shape (example command + output)
- Constraints (performance, determinism, compatibility)

---

## Development setup

### Prerequisites

- Python (see `pyproject.toml` for the current minimum)
- `git`
- Optional: `make`

### Clone

```bash
git clone https://github.com/PhoenixAnvil/data-farm-python.git
cd data-farm-python
```

### Create a virtual environment

```bash
python -m venv .venv

# Windows PowerShell
. .\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate
```

### Install dependencies (dev)

```bash
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

---

## Tooling & quality gates

This repo uses **pre-commit** hooks to keep formatting/lint/testing consistent.

### Install hooks

```bash
pre-commit install
```

### Run hooks manually

```bash
pre-commit run --all-files
```

### Formatting (Black)

```bash
black .
```

### Linting (Ruff)

```bash
ruff check . --fix
```

### Tests (pytest)

```bash
pytest
```

---

## Running Data Farm locally

After an editable install, you can run:

```bash
dfarm --help
```

If you add a new command/flag, please include a minimal example in `examples/` or docs.

---

## Branches, commits, PRs

### Branch naming

Use short, readable names:

- `bugfix/<short-description>`
- `feature/<short-description>`
- `docs/<short-description>`
- `test/<short-description>`
- `refactor/<short-description>`

Examples:

- `bugfix/inspect-null-schema`
- `feature/planner-uuid`
- `docs/cli-examples`

### Commits

Keep commits small and focused:

- One logical change per commit
- Message explains the “why” (not just “what”)
- Prefer reviewable diffs over “mega commits”

### Pull request checklist

Before opening a PR:

- [ ] Tests added/updated (if behavior changes)
- [ ] `pytest` passes locally
- [ ] `pre-commit run --all-files` passes
- [ ] Docs updated if behavior/CLI changes
- [ ] No secrets in configs/logs

In the PR description, include:

- What changed and why
- Link to the issue (e.g., `Closes #123`)
- Design notes / tradeoffs (if relevant)

---

## Design expectations (Data Farm style)

Data Farm aims to stay:

- **Deterministic** (seeded/repeatable output where applicable)
- **CLI-friendly** (clear messages, helpful errors, good exit codes)
- **Testable** (logic in functions/classes; thin CLI boundary)
- **Readable** (clarity over cleverness)

If you’re adding a new generator/planner/suggestor:

- Include tests that validate the contract/invariants
- Include at least one realistic example (docs/examples)
- Consider performance (avoid per-row heavy work if you can)

---

## Security

If you believe you’ve found a security issue (secrets exposure, unsafe file handling, etc.), please **do not** open a public issue.

Follow the contact instructions in `CODE_OF_CONDUCT.md`.

---

## License

By contributing, you agree that your contributions will be licensed under the **MIT License** used by this project.
