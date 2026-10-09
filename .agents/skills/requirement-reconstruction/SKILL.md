---
name: requirement-reconstruction
description: Reconstruct the confirmed brief and fragmented user statements into semantically traceable requirements, a GoalContract, an optional broad-domain CoverageContract, and a WorkPackageGraph. Use when requirements, coverage, or acceptance conditions are new or materially changed; do not create executable tasks, discover sources, or write external knowledge applications.
---

# Requirement Reconstruction

Preserve the user's actual meaning while giving Codex a coherent internal execution model.

## Required References

Read [workflow-contracts.md](../../references/workflow-contracts.md) before handoff. Read [requirement-schema.md](../../references/requirement-schema.md) before creating or revising the GoalContract or WorkPackageGraph. Read [curriculum-coverage-policy.md](../../references/curriculum-coverage-policy.md) for `coverage_first` work. Read [question-gates.md](../../references/question-gates.md) only when a material ambiguity may require the user.

## Preconditions

Require a current IntentContract, SourcePolicy, ProjectContext, ScopeDecisionLedger, and the raw user statements with their conversation, file, or selection anchors. Integrate approved ReuseLineage when applicable. For `coverage_first` work, also require a current CoverageProfile and CoverageBaseline. If structural sources are still pending, return `needs_replan` to the orchestrator with `zotero-source-gate` as the recommended owner rather than inventing a domain boundary from memory.

## Reconstruction

1. Preserve each raw fragment and split compound statements without losing qualifiers, examples, exceptions, or strength.
2. Compare every normalized clause with both the raw fragment and ScopeDecisionLedger. Classify the semantic transformation as preserve, expand, narrow, exclude, or infer.
3. Reject a narrowing or exclusion that lacks explicit user or governing-policy authority, even when it already appears in an upstream artifact. This is semantic provenance, not pointer provenance.
4. Classify requirements and record dependencies, conflicts, executor boundaries, and acceptance evidence.
5. Reconstruct Goal, Outcomes, Deliverables or Capabilities, Milestones, and Work Packages. Keep coverage breadth independent from per-topic mastery depth.
6. For `coverage_first` work, reconcile the confirmed brief with the CoverageBaseline and produce a CoverageContract that defines completeness, topic visibility, depth allocation, prerequisite policy, authorized exclusions, and invalidation conditions.
7. For `large_publication` work, preserve every explicit substantive topic and detail as a traceable content obligation or an explicitly governed conflict. Record the requested scale, full-book completion condition, and the default that exercises do not unlock later publication unless the user chose an interactive course.
8. Map every required condition to a Work Package or explicit invariant.
9. Detect contradictions, uncovered acceptance tests, cycles, untraceable additions, and untraceable scope reductions.
10. Resolve ordinary implementation choices autonomously from the confirmed brief.

Do not ask the user to approve requirement YAML, a goal file, a WorkPackageGraph, or routing choices. Ask one concise Codex question only when the unresolved choice would change the goal, acceptance test, priority, source boundary, risk, or user/AI responsibility.

## Boundaries

- Do not turn illustrative examples into universal domain constraints.
- Do not erase superseded requirements; preserve their lineage internally.
- Do not create hybrid executable tasks. Outcome Orchestrator later assigns each task a knowledge or product mode.
- Do not treat reading, collecting, summarizing, or publication as mastery evidence.
- Do not discover evidence or mutate external applications.
- Do not use `coverage_complete` as a synonym for mapped requirements. Report `requirements_coverage_complete` for internal requirement coverage, and reserve `coverage_verified` for a framework that passes the external coverage audit.
- Do not turn `not required for mastery` into a non-goal or omission without separate authority.
- Do not replace detailed user-specified knowledge with a shorter category label. The original anchors must remain available to the framework and, for a large publication, to `large-publication-architect`.

## Outputs

Internally produce RequirementContract, canonical GoalContract, acyclic WorkPackageGraph, semantic trace map, source gaps, unresolved material conflicts, and a CoverageContract when coverage-first applies. Return them to `knowledge-product-orchestrator` with `ready`, `needs_question`, `needs_replan`, or `blocked`. The normal next owners are Framework and Outcome, selected by the orchestrator.
