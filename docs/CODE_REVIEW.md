# Data Farm Python — Code Review for Open Source Release

**Review date:** February 16, 2025  
**Scope:** All `.py` files under `src/data_farm`, and root config (`pyproject.toml`).  
**Goal:** Polish, professionalism, and high quality to attract contributors. No code was changed; this document is a checklist for you to act on.

---

## How to use this document

- **Checkboxes:** Use `- [ ]` / `- [x]` to track progress (or open in Word and use its checklist).
- **Sections:** Critical bugs first, then design/structure, then style and nitpicks.
- **References:** File paths and line numbers are approximate; use your IDE to jump.

---

## 1. Critical bugs and correctness

### 1.1 CLI dispatch: “app” and “random” commands do nothing

- **File:** `src/data_farm/cli/cli_dispatch.py`
- **Issue:** Branching uses `if ns.command == "project":` then `elif ns.command == "inspect":`. The **“app”** branch only has a comment (“Do we even need this?”) and no behavior. The **“random”** command is never handled, so `dfarm random -s 123` has no effect.
- **Action:**
  - [ ] Either implement “app” (apply config overrides and persist) or remove the subparser and any dead branch.
  - [ ] Either implement “random” (e.g. set/store seed) or remove the subparser.
  - [ ] Use consistent `if`/`elif`/`else` so every command is handled or explicitly rejected.

### 1.2 NameError in `build_conn_url`: `username` / `password` may be undefined

- **File:** `src/data_farm/utils/database.py`
- **Issue:** `username` and `password` are only set inside `if user_env:` and `if password_env:`. When those config keys are absent, the variables are never defined but are used in `kwargs` (e.g. `"username": username`), causing **NameError** at runtime.
- **Action:**
  - [ ] Initialize before the conditionals, e.g. `username = None` and `password = None`, then set them inside the `if` blocks. Ensure `URL.create(**kwargs)` accepts None for these (it does for SQLAlchemy URL).

### 1.3 Config key mismatch: data source config vs. database module

- **File:** `src/data_farm/utils/config.py` vs. `src/data_farm/utils/database.py`
- **Issue:** `default_data_source_config` uses `"user_env_var"` and `"password_env_var"`, but `database.build_conn_url` uses `_optional_str(config, "user_env")` and `"password_env"`. Keys don’t match, so env-based auth will not work with the default template.
- **Action:**
  - [ ] Align keys: either rename in `default_data_source_config` to `user_env` / `password_env`, or use the same keys in `database.py`. Document the expected shape of data source config (e.g. in a docstring or schema).

### 1.4 F-strings not used in exception messages

- **File:** `src/data_farm/utils/config.py`
- **Issue:** `make_data_farm_data_dir` and `make_data_farm_config_dir` raise `ValueError("Could not create ... {p}.")` — the `{p}` is literal, not interpolated.
- **Action:**
  - [ ] Use f-strings: `f"Could not create data dir for data farm: {p}."` and the same for config dir.

### 1.5 Inspect CLI options `--table` and `--rows` are ignored

- **File:** `src/data_farm/cli/base.py`, `src/data_farm/cli/handle_inspect.py`
- **Issue:** The “inspect” subparser defines `-t`/`--table` and `-r`/`--rows`, but `handle_inspect` never uses `ns.table` or `ns.rows`. All tables are inspected and row count is not used for limiting output.
- **Action:**
  - [ ] Either implement filtering by `ns.table` and limiting output with `ns.rows`, or remove these arguments and update help text so users aren’t misled.

### 1.6 Wrong `data_type` for integer column output

- **File:** `src/data_farm/planners/int_planner.py`
- **Issue:** `ColumnEmitDefinition` is built with `data_type=SqlType.STRING` (line 44). Integer columns should emit `SqlType.INTEGER` so the SQL emitter and any downstream logic treat them as integers.
- **Action:**
  - [ ] Use `data_type=SqlType.INTEGER` in `IntPlanner.plan()`.

### 1.7 BooleanPlanner strategy key copy-paste error

- **File:** `src/data_farm/planners/boolean_planner.py`
- **Issue:** `_pattern_key_for_strategy` returns `"ages"` when strategy is `"age"` — clearly copied from IntPlanner. For `"bool"` it should return something like `"bools"` or `None` (and the fallback pattern is already correct).
- **Action:**
  - [ ] Fix `_pattern_key_for_strategy` for BooleanPlanner: e.g. for `"bool"` return `"bools"` or `None`; remove the `"age"` branch.

### 1.8 `FilePathValidator`: wrong f-string in directory error

- **File:** `src/data_farm/utils/path.py`
- **Issue:** `raise ValueError("Source path is not a directory: {path}.")` — `{path}` is not interpolated.
- **Action:**
  - [ ] Use `f"Source path is not a directory: {path}."`.

### 1.9 `NumericFieldDefinition` does not call `super().__init__`

- **File:** `src/data_farm/field/numeric.py`
- **Issue:** Subclass of `FieldDefinition` sets `min_value`/`max_value` but never calls `super().__init__(allow_null=...)`. If `FieldDefinition` gains required logic or args, this will break; also inconsistent with `TextFieldDefinition`.
- **Action:**
  - [ ] Call `super().__init__(allow_null=False)` (or an appropriate default) and pass through `allow_null` if you add it as a parameter.

---

## 2. Project structure and packaging

### 2.1 Missing `__init__.py` (namespace packages)

- **Location:** All packages under `src/data_farm/`
- **Issue:** No `__init__.py` files were found in `app`, `cli`, `emitters`, `errors`, `field`, `generators`, `messages`, `models`, `patterns`, `planners`, `schema`, `suggestors`, `utils`, or `data_farm` itself. Without them, directories are namespace packages (PEP 420). That can work on Python 3.3+ but is not the usual layout for a single, intentional package and can confuse tooling and contributors.
- **Action:**
  - [ ] Add `__init__.py` (even empty) to `src/data_farm` and to every subpackage you intend as a normal package. Optionally re-export public API in `src/data_farm/__init__.py` (e.g. `main`, key types) for a cleaner top-level API.

### 2.2 Misleading module name: `app/init.py`

- **File:** `src/data_farm/app/init.py`
- **Issue:** The file is named `init.py` instead of `__init__.py`. It is app initialization logic, not the package initializer. The name suggests “initialization” but is easy to confuse with `__init__.py`.
- **Action:**
  - [ ] Rename to something like `app/bootstrap.py` or `app/context.py` and update imports (e.g. in `cli_dispatch.py`, `handle_project.py`) to the new module name. Add `app/__init__.py` if you want `app` to be a regular package.

### 2.3 Inconsistent import of `ColumnEmitDefinition`

- **Files:** Multiple (e.g. `handle_inspect.py`, `planners/*.py`, `protocols.py`, `emitters/sql.py`)
- **Issue:** `ColumnEmitDefinition` lives in `data_farm.models.models`. Some code imports it from `data_farm.emitters.sql` (which re-exports it). This blurs the boundary between “model” and “emitter” and makes the canonical home unclear.
- **Action:**
  - [ ] Import `ColumnEmitDefinition` from `data_farm.models.models` (or from `data_farm.models` if you add a package-level re-export) everywhere. Remove the re-export from `emitters/sql.py` to avoid confusion.

### 2.4 Duplicated “default registry” pattern

- **Files:** `planners/registry.py`, `suggestors/defaults.py`, `schema/registry.py`
- **Issue:** Each area has its own registry and “default” construction. That’s fine, but the patterns are slightly different (class method vs. free function, etc.). For contributor clarity, consider a short “Registry pattern” note in the docs or a single, small shared pattern (e.g. a mixin or base) if you want consistency.
- **Action:**
  - [ ] (Optional) Document the intended registry pattern in `docs/` or add a minimal shared abstraction if you want one style across planners/suggestors/schema.

---

## 3. Type hints and protocols

### 3.1 AppNamespace protocol doesn’t match argparse or AppContext

- **File:** `src/data_farm/cli/base.py`
- **Issue:** `AppNamespace` defines `config_root` and `data_root`, but the parser uses `--config-dir` and `--data-dir` (so the namespace has `config_dir`, `data_dir`). `AppContext` also uses `config_dir` and `data_dir`. The protocol is therefore wrong and misleading for type checkers and readers.
- **Action:**
  - [ ] Change `AppNamespace` to use `config_dir` and `data_dir` so it matches the parser and `AppContext`.

### 3.2 Unused dataclasses: `InspectArgs`, `ProjectArgs`

- **File:** `src/data_farm/cli/base.py`
- **Issue:** `InspectArgs` and `ProjectArgs` are defined but never used; dispatch uses `Namespace` and protocol types instead. Dead code.
- **Action:**
  - [ ] Either use these dataclasses (e.g. convert namespace to them and pass around) or remove them to reduce noise.

### 3.3 Return type of `handle_inspect`

- **File:** `src/data_farm/cli/handle_inspect.py`
- **Issue:** No return type annotation. Should be `-> None` for consistency and tooling.
- **Action:**
  - [ ] Add `-> None` to `handle_inspect`.

### 3.4 Abstract methods using `pass` instead of `...`

- **Files:** e.g. `schema/base.py`, `emitters/base.py`, `generators/base.py`, `suggestors/base.py`
- **Issue:** Abstract methods use `pass`. The more idiomatic and minimal body for abstracts is `...` (Ellipsis).
- **Action:**
  - [ ] Replace `pass` in abstract method bodies with `...` for consistency with common Python style.

---

## 4. Naming and readability

### 4.1 Cryptic variable names in `handle_inspect`

- **File:** `src/data_farm/cli/handle_inspect.py`
- **Issue:** Names like `pp`, `ppp`, `acp`, `ac`, `psd`, `pd`, `ed`, `e`, `preg`, `pctx` hurt readability and maintainability.
- **Action:**
  - [ ] Replace with descriptive names, e.g. `project_path` → variable for path, `app_config_path`, `app_config`, `projects_root_dir`, `project_dir`, `emit_defs`, `emitter`, `planner_registry`, `plan_context`. Use one or two clear words per variable.

### 4.2 Short names in `app/init.py`

- **File:** `src/data_farm/app/init.py`
- **Issue:** Abbreviations like `cr`, `dr`, `cp`, `dcd`, `cd` are used throughout. Fine for very local, tiny scope; here they span the whole function and make the flow harder to follow.
- **Action:**
  - [ ] Use at least `config_dir`, `data_dir`, `config_path`, `default_config`, `loaded_config` (or similar) so intent is clear.

### 4.3 Shadowing built-in / standard name in `build_parser`

- **File:** `src/data_farm/cli/base.py`
- **Issue:** `random = subparsers.add_parser("random", ...)` shadows the imported `random` module. Any later use of `random` in that function would refer to the subparser, not the module.
- **Action:**
  - [ ] Rename the variable, e.g. `random_parser = subparsers.add_parser("random", ...)`.

### 4.4 Single-letter or opaque names in planners and suggestors

- **Files:** e.g. `string_planner.py` (`s`), `builtins.py` (`n`, `t`, `c`), `engine.py` (`s`), `suggestors/fallback.py` (`t`, `n`)
- **Issue:** In small blocks it’s acceptable, but in longer or shared code, names like `s` (strategy), `n` (name), `t` (type), `c` (confidence/column) can be clarified.
- **Action:**
  - [ ] Where it improves clarity, use `strategy_clean`, `col_name`, `sql_type`, `column` (or similar) so the role of each variable is obvious.

---

## 5. Duplication and reuse

### 5.1 Repeated planner “pattern + TextGenerator” pattern

- **Files:** `string_planner.py`, `numeric_planner.py`, `boolean_planner.py`, `int_planner.py`
- **Issue:** All planners share a pattern: resolve pattern (from strategy or fallback), build `TextFieldDefinition`, call `TextGenerator(...).generate()`, then build `ColumnEmitDefinition`. Only the strategy key, fallback pattern, and `SqlType` differ. This is a lot of duplicated structure.
- **Action:**
  - [ ] Consider a small helper (e.g. in `planners/common.py` or a base class) that takes strategy key, fallback pattern, and `SqlType`, and returns `ColumnEmitDefinition | None`, so each planner only supplies those three things. Reduces duplication and keeps behavior consistent.

### 5.2 `_pattern_key_for_strategy` duplicated across planners

- **Files:** `string_planner.py`, `numeric_planner.py`, `boolean_planner.py`, `int_planner.py`
- **Issue:** Each planner has a similar `_pattern_key_for_strategy(strategy) -> str | None` with different mappings. The logic is the same; only the mapping differs.
- **Action:**
  - [ ] Consider a single helper (e.g. on a base class or in a shared module) that takes a mapping `strategy -> pattern_key` and the strategy string, and returns the pattern key. Each planner then only defines its mapping.

### 5.3 Redundant `Path()` wrapping

- **File:** `src/data_farm/cli/handle_project.py`
- **Issue:** `create_project_structure` does `p = Path(path)` even when `path` is already a `Path` in callers. Defensive but redundant if the type contract is `Path`.
- **Action:**
  - [ ] Type the parameter as `Path` and avoid re-wrapping when the caller already passes a `Path`; or document that both `Path` and path-like are accepted and normalize once at the start.

### 5.4 Config validation duplication

- **File:** `src/data_farm/utils/config.py`
- **Issue:** `validate_data_source_config` and `validate_data_farm_config` are nearly identical (both only check that config is non-empty). Generic “config not valid” message is also not very helpful.
- **Action:**
  - [ ] Consider a single internal helper (e.g. `_validate_config_non_empty(config, name="config")`) and optionally add more specific checks (required keys, types) and clearer error messages.

---

## 6. Unused or dead code

### 6.1 Unused message module

- **File:** `src/data_farm/messages/messages.py`
- **Issue:** `msg()` and `MESSAGES` exist but are not used. `handle_inspect` uses a hardcoded string for the planner-not-found error instead of `msg("err.planner.not_found", ...)`. `cli.help.rows` is also never used.
- **Action:**
  - [ ] Either wire the CLI and handlers to use `messages.msg()` for user-facing strings (recommended for i18n and consistency), or remove the messages module if you don’t plan to use it.

### 6.2 Stub / unused classes

- **Files:** `generators/numeric.py` (`NumberGenerator`), `generators/dates.py` (`DateGenerator`)
- **Issue:** Both classes are empty stubs (no `generate` implementation, no other methods). They are not referenced anywhere. Same for `NumericFieldDefinition` in `field/numeric.py` — it’s defined but not used in the codebase.
- **Action:**
  - [ ] Either implement and use these types where appropriate, or remove them until needed. If you keep them as placeholders, add a short comment or docstring (e.g. “Reserved for future use”) and a `# noqa` or `raise NotImplementedError` in abstract methods so the intent is clear.

### 6.3 Unused method: `_has_math_symbols`

- **File:** `src/data_farm/schema/database.py`
- **Issue:** `_has_math_symbols` is defined but never called. Dead code.
- **Action:**
  - [ ] Remove it, or use it in type parsing if that was the original intent.

### 6.4 Unused `Pattern.load_from_file`

- **File:** `src/data_farm/patterns/base.py`
- **Issue:** `Pattern` has `load_from_file` and `source_path`, but `PatternRegistry` loads patterns from files itself and builds `Pattern` with `classification` and `choices`. So `load_from_file` appears unused.
- **Action:**
  - [ ] Either use `Pattern.load_from_file` somewhere (and possibly refactor registry to use it), or remove it and the `source_path` field to avoid two ways of loading patterns.

### 6.5 Unused `data_source_config_file_exists`

- **File:** `src/data_farm/utils/config.py`
- **Issue:** `data_source_config_file_exists` is defined but not referenced anywhere.
- **Action:**
  - [ ] Use it where you check for data source config file existence, or remove it.

---

## 7. Error handling and robustness

### 7.1 Bare `except Exception` in main

- **File:** `src/data_farm/main.py`
- **Issue:** `except Exception` then traceback + message + SystemExit(1) catches everything, including `KeyboardInterrupt`. Users expect Ctrl+C to exit cleanly.
- **Action:**
  - [ ] Add `except KeyboardInterrupt` before the generic `Exception` handler and exit with a clean message (e.g. 130 or 1) without full traceback.

### 7.2 DatabaseInspector connection cleanup on error

- **File:** `src/data_farm/schema/database.py`
- **Issue:** In `connect()`, on any exception we call `self.disconnect()` and re-raise. That’s good, but if `disconnect()` itself raises, the original exception is lost. Consider `try/finally` or ensuring `disconnect()` never raises for cleanup.
- **Action:**
  - [ ] (Optional) Wrap `disconnect()` in a try/except in cleanup paths so the original error is always propagated; log any disconnect error.

### 7.3 `validate_data_source_config` / `validate_data_farm_config` too weak

- **File:** `src/data_farm/utils/config.py`
- **Issue:** Validation only checks that the config dict is non-empty. Missing required keys (e.g. `data_source`, `source_type`, `driver`) cause later `KeyError` or `ValueError` with less clear messages.
- **Action:**
  - [ ] Validate required top-level keys and, if applicable, nested keys (e.g. `data_source.driver`, `project.projects_root`) and raise with clear messages (e.g. “Missing required key 'data_source' in config”).

---

## 8. Docstrings and comments

### 8.1 Placeholder docstrings “TBD”

- **Files:** Many (e.g. `models/models.py`, `emitters/sql.py`, `generators/text.py`, `patterns/base.py`, `schema/base.py`, `schema/database.py`, `field/base.py`, `errors/errors.py`, `utils/config.py`, etc.)
- **Issue:** “TBD” or empty `""" """` docstrings give no guidance to contributors or API users.
- **Action:**
  - [ ] Replace with one-line (or short) summaries for every public class and function. For complex functions (e.g. `_normalize_type`, `_get_type_params`), add a sentence on purpose and return value. Prefer “Summary.” style (capital, period).

### 8.2 Incorrect module path in comment

- **File:** `src/data_farm/models/models.py`
- **Issue:** First line comment says `# data_farm/suggestors/model.py` but the file is `models/models.py`.
- **Action:**
  - [ ] Fix to `# data_farm/models/models.py` or remove the comment.

### 8.3 Redundant or noisy comments

- **Files:** e.g. `planners/registry.py` (“# adjust import”), `planners/int_planner.py` (“# adjust import”), etc.
- **Issue:** “adjust import” looks like a todo or leftover note.
- **Action:**
  - [ ] Remove or replace with a meaningful comment (e.g. why a lazy import is used).

---

## 9. Python idioms and style

### 9.1 Use of `list` instead of `list[...]` (Python 3.9+)

- **Files:** Various
- **Issue:** You already use `list[...]` and `dict[str, Any]` in many places, which is good. Ensure consistency (e.g. no remaining `List` from typing unless you support older Python).
- **Action:**
  - [ ] Grep for `from typing import List` or `List[` and replace with `list[` and drop the import if nothing else needs it. You’re on 3.10+ so built-in generics are fine.

### 9.2 Prefer `pathlib` over `os` where possible

- **File:** `src/data_farm/utils/database.py`
- **Issue:** Uses `os.environ.get`. That’s fine; for path construction the codebase already uses `Path`. No change needed for env; just keep path logic on `Path`.
- **Action:**
  - [ ] (Optional) Document that path handling should use `pathlib`; no code change required if already consistent.

### 9.3 PatternRegistry default for `_cache`

- **File:** `src/data_farm/patterns/registry.py`
- **Issue:** `field(default_factory=lambda: {})` can be written as `field(default_factory=dict)` — simpler and idiomatic.
- **Action:**
  - [ ] Use `default_factory=dict`.

### 9.4 Boolean conversion

- **File:** `src/data_farm/patterns/registry.py`
- **Issue:** `exists()` has `if key in self._cache: return True` then `return self._pattern_path(key).exists()`. Can be written as `return key in self._cache or self._pattern_path(key).exists()`.
- **Action:**
  - [ ] Simplify to a single return expression for readability.

### 9.5 Choose best suggestion

- **File:** `src/data_farm/suggestors/engine.py`
- **Issue:** `choose_best` mutates the list with `suggestions.sort(...)`. Callers might not expect mutation. Prefer building a sorted copy or using `min`/max with a key (e.g. `max(suggestions, key=...)`) to avoid side effects.
- **Action:**
  - [ ] Use `best = max(suggestions, key=lambda s: (s.confidence, s.priority))` (and handle empty list before), or sort a copy: `sorted(suggestions, key=..., reverse=True)[0]`, so the original list is unchanged.

### 9.6 SqlEmitter match: use default for unknown types

- **File:** `src/data_farm/emitters/sql.py`
- **Issue:** The `match ed.data_type` has a `case _: out = ""` for unknown types. Emitting an empty string can produce invalid SQL. Consider logging a warning and/or raising an error for unsupported types, or document that unknown types are intentionally omitted.
- **Action:**
  - [ ] Either raise `NotImplementedError` or `ValueError` for unknown types, or document and optionally log when `out = ""` is used.

### 9.7 SQL injection / safety

- **File:** `src/data_farm/emitters/sql.py`
- **Issue:** Table and column names are interpolated into the SQL string. If those ever come from untrusted input, that’s unsafe. For a test-data tool it may be acceptable, but worth documenting.
- **Action:**
  - [ ] In docstring or docs, state that table/column names are expected to be schema-derived (not user input) or add a short note on trusted vs. untrusted input. If you add support for user-provided identifiers later, use proper quoting/identifiers.

---

## 10. pyproject.toml and tooling

### 10.1 Package name vs. import name

- **File:** `pyproject.toml`
- **Issue:** `name = "datafarm"` (no underscore) but the import is `data_farm`. That’s valid (PyPI name can differ from import), but it can confuse contributors.
- **Action:**
  - [ ] In README or contributing guide, state that the PyPI/install name is `datafarm` and the import name is `data_farm`.

### 10.2 Metadata completeness

- **File:** `pyproject.toml`
- **Issue:** No `readme`, `license`, `keywords`, `classifiers`, or `urls` (Homepage, Repository, Documentation). These help discoverability and automation.
- **Action:**
  - [ ] Add `readme = "README.md"`, `license = { text = "MIT" }` (or file), `classifiers = ["License :: OSI Approved :: MIT License", "Programming Language :: Python :: 3", "Programming Language :: Python :: 3.10", ...]`, and `urls = { "Homepage" = "...", "Repository" = "https://github.com/...", "Documentation" = "..." }`.

### 10.3 Optional dev dependencies

- **File:** `pyproject.toml`
- **Issue:** Black and Ruff are configured but not listed as dev dependencies, so new contributors may not have the same formatter/linter.
- **Action:**
  - [ ] Add `[project.optional-dependencies]` (e.g. `dev = ["ruff", "black", "pytest", ...]`) and document `pip install -e ".[dev]"` in CONTRIBUTING or README.

### 10.4 Ruff “PL” rules

- **File:** `pyproject.toml`
- **Issue:** You use a broad “PL” set. Some PL rules can be noisy. Consider enabling specific PL categories (e.g. `PLR`, `PLC`) and ignoring others if you get too many warnings.
- **Action:**
  - [ ] Run `ruff check .` and either fix reported issues or narrow `select`/`ignore` so the rule set is sustainable.

---

## 11. Testing and quality assurance

### 11.1 No tests in scope

- **Location:** Repository root / `tests/`
- **Issue:** No test files were in the reviewed scope. For open source, tests are critical for contributor confidence and refactoring.
- **Action:**
  - [ ] Add a `tests/` directory (or `src/data_farm/tests` if you prefer), pytest (or unittest), and at least: (1) unit tests for planners, suggestors, and config loading; (2) a few integration tests for the inspect flow (e.g. with a SQLite in-memory DB). Document how to run tests in README/CONTRIBUTING.

### 11.2 Type checking

- **Issue:** No `py.typed` or mypy/pyright config was evident. Adding type hints is good; running a static checker ensures they stay correct.
- **Action:**
  - [ ] Add `py.typed` to the package (empty file in `src/data_farm/`). Optionally add `[tool.mypy]` or `[tool.pyright]` in `pyproject.toml` and run in CI.

---

## 12. Security and configuration

### 12.1 Secrets in config

- **Issue:** Database credentials come from env vars (good). Ensure docs and examples never show real credentials and that `data_source_config.toml` is in `.gitignore` if it can contain env var names that might be reused.
- **Action:**
  - [ ] In README or docs, recommend keeping `data_source_config.toml` out of version control when it references env vars with secrets. Add a sample `data_source_config.toml.example` with placeholders.

### 12.2 Seed handling

- **File:** `main.py`, `cli/base.py`, `app/init.py`
- **Issue:** Seed can come from CLI or config. Document that the seed is for reproducibility, not security.
- **Action:**
  - [ ] One-line note in README or config doc: seed is for reproducible data generation, not cryptographic use.

---

## 13. Summary checklist (high level)

- [ ] **Bugs:** Fix dispatch (app/random), `build_conn_url` username/password, config f-strings, path f-string, IntPlanner `SqlType`, BooleanPlanner pattern key, NumericFieldDefinition `super().__init__`.
- [ ] **Structure:** Add `__init__.py` where needed; rename `app/init.py`; standardize `ColumnEmitDefinition` import; optional registry doc or small shared pattern.
- [ ] **Types:** Fix `AppNamespace`; add `handle_inspect` return type; remove or use `InspectArgs`/`ProjectArgs`; use `...` in abstract methods.
- [ ] **Naming:** Improve names in `handle_inspect` and `app/init.py`; avoid shadowing `random` in base.py; clarify short names in planners/suggestors.
- [ ] **Duplication:** Factor common planner logic and `_pattern_key_for_strategy`; unify config validation; reduce redundant `Path()`.
- [ ] **Dead code:** Use or remove messages module; implement or remove stub generators and `NumericFieldDefinition`; remove `_has_math_symbols`; resolve `Pattern.load_from_file` and `data_source_config_file_exists`.
- [ ] **Errors:** Handle `KeyboardInterrupt` in main; tighten config validation; consider error behavior in SqlEmitter for unknown types.
- [ ] **Docs:** Replace “TBD”/empty docstrings; fix models.py comment; remove “adjust import” comments.
- [ ] **Idioms:** `default_factory=dict`; simplify `PatternRegistry.exists`; avoid mutating list in `choose_best`; document SQL identifier trust.
- [ ] **pyproject.toml:** Add readme, license, classifiers, urls; add optional dev deps; document package vs. import name; tune Ruff if needed.
- [ ] **Quality:** Add tests and `py.typed`; document seed and config security briefly.

---

**End of review.** Use this list to work through changes in your own order of priority; addressing Section 1 (Critical bugs) first is recommended.
