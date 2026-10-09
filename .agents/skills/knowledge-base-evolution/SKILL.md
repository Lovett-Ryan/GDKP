---
name: knowledge-base-evolution
description: Evaluate, explain, and reconcile an optional evidence-backed update from current-project knowledge into an existing GDKP knowledge base. Own Q4 and the ordered cross-system change plan; do not write Zotero, Notion, or Obsidian directly, expose machine diffs, or propose updates based only on similarity.
---

# Knowledge Base Evolution

Let useful new knowledge extend an existing knowledge base without turning every similarity into an update or obscuring external origin.

## Required Contracts

Read [workflow-contracts.md](../../references/workflow-contracts.md) before creating a handoff or subflow request. Read [question-gates.md](../../references/question-gates.md) before Q4. Read [reuse-and-evolution-policy.md](../../references/reuse-and-evolution-policy.md) for eligibility, placement, marker, approval, and reconciliation.

## Preconditions

Require distinct current and target ProjectContexts, a current Goal, a Framework-supported semantic relationship, target-compatible evidence, resolvable target bindings, and a proposed smallest suitable target node. Co-occurrence, shared citations, keywords, containers, or page proximity are insufficient.

## Planning

1. Validate the target knowledge base, source policy, managed boundaries, and node and relation revisions.
2. Ask Framework to reserve any missing node, relation, or placement through the orchestrator.
3. Ask Zotero Source Gate to admit evidence under the target policy when needed.
4. Ask Notion Author to prepare the reader-facing addition and route its final fact-bearing wording through the Zotero claim audit.
5. Determine the conservative graph effect and external-increment exclusion.
6. Present Q4 in Codex as a short readable summary: target topic, proposed addition, why it belongs, source lineage, graph impact, marker, and decline option.
7. Do not present nested YAML, a machine diff, claim records, operation receipts, or page previews.

On decline, leave the target unchanged and record `optional_declined`. On approval, create an internal immutable EvolutionChangeSet and ordered owner requests. Q4 authorizes reversible workflow-owned writes for that exact stated change; a destructive, ambiguous, out-of-scope, or user-content-overwriting action requires a new direct decision.

## Reconciliation

After Codex dispatches Lifecycle, Framework, Zotero, Notion, and Obsidian work, confirm target identity, Zotero source admission and claim-audit state, managed boundaries, successful Notion and Obsidian write results, and graph exclusion policy. Do not request Notion or Obsidian content read-back receipts. Report completion only when all required owners have returned their results.

Use the visible default marker `※ External Increment` at the smallest suitable Notion topic. Keep the addition out of the ordinary Obsidian graph while its internal origin status is pending or accepted. Do not invent an automatic promotion policy.

Return `not_applicable`, a prerequisite owner request, `needs_question`, `optional_declined`, an approved EvolutionChangeSet, or a reconciliation result to `knowledge-product-orchestrator`.
