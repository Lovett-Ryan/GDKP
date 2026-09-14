---
name: intent-source-analysis
description: Convert a new or materially changed learning, product, or hybrid request into a confirmed outcome, breadth, depth, and source-policy boundary through one compact Codex conversation. Use after project setup when goal meaning or source scope is missing or stale; do not approve supplemental source candidates, ingest evidence, build the knowledge framework, install Skills, or publish content.
---

# Intent and Source Analysis

Turn an imprecise request into enough shared understanding for Codex to work autonomously across any domain.

## Required References

Read [workflow-contracts.md](../../references/workflow-contracts.md) before producing a handoff. Read [question-gates.md](../../references/question-gates.md) for the compact intake. Use [scenario-catalog.md](../../references/scenario-catalog.md) and the relevant portion of [source-policy-by-domain.md](../../references/source-policy-by-domain.md). Read [curriculum-coverage-policy.md](../../references/curriculum-coverage-policy.md) when the request is a textbook, curriculum, comprehensive survey, field-level learning map, or other broad-domain goal. Read [domain-capability-gap-policy.md](../../references/domain-capability-gap-policy.md) only if a specialized capability may be missing.

## Inputs

Use the user's current request, existing project context, supplied books, papers, sites, courses, videos, repositories, files, records, or data, plus relevant language, date, version, region, jurisdiction, access, budget, confidentiality, and risk constraints.

Do not assume the domain is AI, research, or computing. Recognize engineering, mathematics, medicine, social science, business, law, humanities, daily life, broad products, and novel scenarios equally.

## Compact Intake

Ask only for facts that are missing and materially affect the path. In one short exchange when possible, confirm:

1. learning, product, or hybrid intent;
2. the observable result and acceptance condition;
3. user-selected sources and their intended role;
4. permission and limits for supplemental discovery;
5. user-reserved decisions or work.

For `coverage_first` work, confirm or safely derive coverage breadth separately from learning depth. A request for comprehensive awareness plus mastery of selected topics means the broad field remains visible while depth varies by topic. Weak foundations change scaffolding and order, not breadth. If a plausible normalization would remove major topics, ask rather than narrowing silently.

Use the host Question mechanism when available; otherwise ask directly at the end of the turn. Never publish the question or its answer to Notion or Obsidian. Do not show the internal IntentContract or SourcePolicy for approval.

## Source Rules

- Mark user-selected sources as `user_primary` and pre-authorized for project Zotero registration.
- Record evidence quality separately from user priority.
- Explain meaningful weakness, age, conflict, access, version, or jurisdiction risk without silently replacing a user source.
- Define authoritative source classes for knowledge work or sources closest to the requested product and environment for product work.
- Allow `zotero-source-gate` to present one later concrete shortlist only for AI-suggested supplements.
- Assign structural sources a distinct `structural_baseline` role when they are intended to define curriculum coverage. They do not support chapter claims merely because their table of contents or taxonomy was used.

## Scope Fidelity

Create a revisioned ScopeDecisionLedger for material normalizations. Record the raw fragment, normalized clause, transformation type, authority, confidence, question state, and affected artifacts. Preserve explicit qualifiers in both directions.

A narrowing or exclusion requires an explicit user statement or named governing policy. AI judgment may propose but cannot confirm it. In particular, do not infer any of the following:

- selective mastery narrows the visible knowledge map;
- a beginner needs only a minimal topic inventory;
- a request that is not literally exhaustive permits omission of major canonical branches;
- a framework-confirmation request prohibits the structural-source work needed to make that framework complete.

When a coverage-first trigger is present, emit a CoverageProfile containing the genre, breadth, depth policy, structural-source state, and current coverage confidence. If authoritative structural sources are still needed, recommend `zotero-source-gate` before requirement reconstruction.

## Capability Hint

Compare the confirmed outcome with active project capabilities. Report a capability-gap hint only when a missing specialized method, standard, validation protocol, format, or tool could affect an acceptance test. Do not search GitHub or ask Q5.

## Outputs

Internally produce a revisioned IntentContract, SourcePolicy, ScopeDecisionLedger, and, when applicable, CoverageProfile, plus any capability-gap or reuse hint. Return `ready`, `needs_question`, or `needs_replan` to `knowledge-product-orchestrator`. `ready` means the brief is sufficiently clear; it does not mean coverage has been verified. Use `coverage_unverified` inside the CoverageProfile until a current structural baseline and coverage audit exist.
