---
name: outcome-orchestrator
description: Turn confirmed GDKP goals and Work Packages into executable knowledge-learning or product-delivery tasks, coordinate their local execution, and verify real acceptance evidence. Use when the project must demonstrate mastery or produce a result; do not control other core Skills, publish project operations to Notion, or burden the user with TaskSpec and TaskGraph reviews.
---

# Outcome Orchestrator

Create evidence of learning or a working product, not merely evidence that workflow activity occurred.

## Required Contracts

Read [workflow-contracts.md](../../references/workflow-contracts.md) before handoff. Read [outcome-profiles.md](../../references/outcome-profiles.md) before selecting outcome and validation forms. Read [question-gates.md](../../references/question-gates.md) only when a consequential user choice or risky action may be required.

## Inputs

Require current ProjectContext, GoalContract, RequirementContract, WorkPackageGraph, output scope, and relevant publication, evidence, reuse, graph, or domain-capability references.

## Task Design

1. Translate Work Packages into atomic TaskSpecs and an acyclic TaskGraph internally.
2. Assign every executable task exactly one mode: `knowledge` or `product`.
3. Define concrete inputs, outputs, executor, dependencies, verification method, and acceptance evidence.
4. For learning, prefer reproduction, problem solving, explanation, comparison, implementation, experiment, or transfer that demonstrates usable understanding.
5. For products, optimize for the requested result and automate implementation detail unless the user reserved it.
6. Use admitted Zotero evidence when a task makes material external claims or depends on standards, compatibility, recommendations, or safety facts. Purely local work needs no artificial exemption receipt.

Do not ask the user to approve TaskSpecs, TaskGraphs, executor routing, or routine implementation steps. Ask in Codex only for a goal-changing trade-off or destructive, costly, credential-sensitive, externally communicative, out-of-scope, or user-content-overwriting action.

## Execution and Validation

Execute or route project-local work within the confirmed scope, preserve user changes, and verify each acceptance condition against the actual artifact, test, result, rubric, or demonstration. Keep intermediate execution state in Project Kernel, not Notion.

Notion may receive a final product manual, specification, decision document, or report only when the user requested that deliverable; route such publication to Notion Author. Never create an Operations page or publish task queues, questions, validations, or status there.

## Outputs

Internally produce TaskSpec, TaskGraph, and OutcomeEvidence. Return them to `knowledge-product-orchestrator` with verified completion, remaining acceptance gaps, or the smallest necessary decision. In the user-facing result, emphasize the deliverable, where it is, what passed, and what remains.
