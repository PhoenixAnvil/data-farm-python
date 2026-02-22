Data Farm Architecture
======================

Overview
--------

Data Farm is a schema-aware test data generation tool built around a
staged pipeline architecture. Each stage is responsible for a single,
well-defined transformation in the process of converting database
schema metadata into generated output.

The system is intentionally layered to enforce separation of concerns.
No stage performs the responsibilities of another. This makes the tool
predictable, testable, and extensible without requiring modifications
to the core pipeline.

At a high level, the generation flow is:

    Inspector → Suggestor → Planner → Generator → Emitter


Pipeline Stages
---------------

Inspector
~~~~~~~~~

The Inspector is responsible for reading a target data source and
producing inspection models that describe its structure.

Responsibilities:

- Connect to a data source.
- Read schema metadata (tables, columns, constraints, types).
- Produce structured inspection models for downstream processing.

The Inspector does **not**:

- Generate values.
- Decide generation strategies.
- Emit SQL or other output formats.

Its role is purely observational. It translates external structure into
internal models.


Suggestor
~~~~~~~~~

The Suggestor determines which generation strategy should be applied to
each inspected column.

Responsibilities:

- Analyze column metadata.
- Select an appropriate generation strategy.
- Produce strategy definitions for planners.

The Suggestor does **not**:

- Generate actual values.
- Emit output.
- Execute generation logic.

This stage separates *strategy selection* from *strategy execution*.
By isolating this decision point, Data Farm avoids embedding conditional
dispatch logic throughout the pipeline.


Planner
~~~~~~~

The Planner converts a chosen strategy into executable generation logic.

Responsibilities:

- Translate strategy definitions into value-generation behavior.
- Operate deterministically when provided a random number generator.
- Remain stateless once constructed.

Planners are pure execution units. Given the same configuration and
random seed, they produce the same output.

Planners do **not**:

- Inspect schemas.
- Choose strategies.
- Emit SQL or write files.

They are responsible only for producing values.


Generator
~~~~~~~~~

The Generator orchestrates planner execution.

Responsibilities:

- Execute planners repeatedly for a specified number of rows.
- Coordinate value generation across columns.
- Produce row-level value sets.

The Generator does not know how strategies are chosen or how values are
ultimately emitted. It simply drives the execution of planners to produce
structured row data.


Emitter
~~~~~~~

The Emitter transforms generated row data into a concrete output format.

Responsibilities:

- Convert row-level values into SQL INSERT statements or other formats.
- Handle formatting, escaping, and output structure.
- Write output to stdout or files.

The Emitter does not generate values and does not inspect schemas. It
is concerned only with representation.


Design Principles
-----------------

Separation of Concerns
~~~~~~~~~~~~~~~~~~~~~~

Each stage has a single responsibility. This prevents leakage of logic
across boundaries and makes the system easier to reason about and test.


Deterministic Randomness
~~~~~~~~~~~~~~~~~~~~~~~~

All randomness is controlled through explicit random number generator
instances. Given the same seed and configuration, Data Farm produces
identical output. This makes generated data reproducible for testing
and debugging.


Registry-Based Extensibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Strategies and planners are resolved through registry mechanisms rather
than conditional dispatch trees. New planners can be added without
modifying core pipeline logic.


Explicit Contracts
~~~~~~~~~~~~~~~~~~

Each stage defines a clear contract:

- Inspectors produce inspection models.
- Suggestors produce strategy definitions.
- Planners produce values.
- Generators produce rows.
- Emitters produce formatted output.

These contracts enforce clarity and prevent cross-stage coupling.


Extending Data Farm
-------------------

To introduce new generation behavior:

1. Implement a new planner.
2. Register the planner in the appropriate registry.
3. Ensure the Suggestor maps relevant schema patterns to the new strategy.

No modification to the pipeline stages is required. The architecture
is designed to support growth without structural changes.
