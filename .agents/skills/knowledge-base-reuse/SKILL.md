---
name: knowledge-base-reuse
description: Discover and establish traceable reuse of a qualified existing GDKP knowledge base when reuse could materially help the current goal. Own the optional Q3 decision and reuse lineage; do not inspect full candidate content before approval, modify the source knowledge base, publish copied content, or force reuse when independent work is viable.
---

# Knowledge Base Reuse

Reuse existing knowledge without hiding its origin, freshness, evidence scope, or limitations.

## Required Contracts

Read [workflow-contracts.md](../../references/workflow-contracts.md) before handoff. Read [question-gates.md](../../references/question-gates.md) before Q3. Read [reuse-and-evolution-policy.md](../../references/reuse-and-evolution-policy.md) for qualification, reuse modes, lineage, and invalidation.

## Preconditions

Require current ProjectContext, GoalContract, SourcePolicy, and workspace-registry revision. Act when the user explicitly requests reuse or registry metadata reveals a candidate with meaningful goal coverage.

## Workflow

1. Search metadata only and qualify candidates by coverage, freshness, source lineage, scope compatibility, resolvable bindings, conflicts, and limitations.
2. Do not ask Q3 when no candidate qualifies; return `no_candidate` and let the project build independently.
3. For qualified candidates, show a concise natural-language Q3 summary in Codex. Do not show registry YAML or lineage schemas.
4. Offer reference, snapshot, fork, partial reuse, or no reuse.
5. On decline, record `optional_declined` internally and continue independently without persuasion.
6. On approval, read only the authorized scope, verify revisions and source lineage, and create internal ReuseLineage.
7. Return the lineage through the orchestrator to Requirement Reconstruction before dependent Framework or Outcome work proceeds.

## Boundaries

- Reuse approval does not authorize mutation of the source knowledge base.
- A fork creates new project-owned material through the normal Framework, Zotero, and Notion owners; this Skill does not copy or publish it.
- Do not treat a broad label, shared keyword, or stale inaccessible registry entry as a qualified candidate.
- Invalidate or re-ask only when goal coverage, selected scope, source or publication revision, conflicts, or reuse mode materially changes.

Return `ready`, `needs_question`, `optional_declined`, `no_candidate`, or `needs_replan` inside a standard handoff to `knowledge-product-orchestrator`.
