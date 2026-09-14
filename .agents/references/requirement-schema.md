# Requirement and Goal Model

Requirement reconstruction is an internal reasoning step. Its structured artifacts support scheduling and recovery; they are not documents the user must review.

## Raw Fragments

Preserve each user statement with its conversation, file, or selection anchor. Split compound statements into atomic requirements while retaining qualifiers, examples, exceptions, and strength.

Classify requirements as goal, deliverable, constraint, source rule, content rule, graph rule, user-decision rule, or acceptance condition. Every normalized requirement must trace to at least one raw fragment.

Traceability includes semantic direction, not merely a pointer to an upstream artifact. Compare each normalized clause with the raw fragment and current ScopeDecisionLedger. Mark whether it preserves, expands, narrows, excludes, or infers meaning. Words such as `core`, `minimum`, `bounded`, `selected`, `optional`, `deferred`, and `not exhaustive` are material when they change coverage. A narrowing or exclusion without explicit user or governing-policy authority is an unresolved conflict, even when an upstream IntentContract already contains it.

## Goal Contract

The GoalContract records internally:

- a concise objective and mode: knowledge, product, or hybrid;
- observable outcomes and deliverables;
- acceptance tests;
- non-goals and exclusions;
- source and risk boundaries;
- the user's required involvement;
- revision and invalidation conditions.

`requirement-reconstruction` is the sole owner of the canonical GoalContract. The initial brief supplies its approved meaning; no separate GoalContract approval is required unless reconstruction exposes a material ambiguity or contradiction.

For a `coverage_first` goal, keep breadth and mastery as separate GoalContract dimensions. `Not required for mastery` is not a non-goal unless the user or governing policy separately excludes it from the visible field map.

## Coverage Contract

Read [curriculum-coverage-policy.md](curriculum-coverage-policy.md) for a textbook, curriculum, broad field map, or other coverage-first project. The CoverageContract binds the confirmed breadth profile to the current CoverageBaseline and records:

- the project-specific meaning of completeness;
- topic classes that must remain visible;
- depth-allocation and prerequisite rules;
- source, version, and recency boundaries;
- authorized exclusions;
- coverage acceptance tests and invalidation conditions.

The CoverageContract may remain provisional while structural sources are pending. Do not label a project `coverage_verified` from raw requirements alone. A `local_files_verified` baseline may support a confirmed contract and later `coverage_local_verified` framework audit, but that status retains its source-admission and factual-evidence limitations.

## Work Packages

Build an acyclic WorkPackageGraph that maps each required outcome to coherent internal work. A Work Package is not an executable task and is never shown for routine approval. Each package records its goal and requirement lineage, inputs, expected output, dependencies, owner class, and acceptance evidence.

Every `must` requirement must map to a Work Package or a named system invariant. Detect uncovered acceptance tests, dependency cycles, conflicts, and additions that cannot be traced to user intent.

Report `requirements_coverage_complete` for this check. Never shorten that state to `coverage_complete` because it could be mistaken for externally grounded domain completeness.

## Questions

Ask only when the unresolved choice would materially change the objective, acceptance test, priority, source boundary, risk, or user/AI responsibility. Present the concrete ambiguity in natural language in Codex. Do not ask the user to validate IDs, graph topology, schema fields, or executor routing.

## Mode Semantics

A hybrid project may contain both learning and product outcomes. Each executable task later created by Outcome Orchestrator is exactly `knowledge` or `product` so its completion evidence remains clear.

Reading, collecting, summarizing, or publishing is not by itself proof of learning. Likewise, an activity log is not proof that a product meets its acceptance tests.

## Revision

Preserve superseded requirements and trace why they changed. Reconstruct after a material goal change, accepted reuse lineage, or a conflict that changes scope. Do not trigger reconstruction for stylistic publication feedback or ordinary source substitution that leaves the goal unchanged.

A new or materially revised CoverageBaseline also invalidates the CoverageContract and every dependent framework coverage audit, even when the user's prose goal is unchanged.
