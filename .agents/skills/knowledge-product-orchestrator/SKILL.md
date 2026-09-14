---
name: knowledge-product-orchestrator
description: Coordinate the end-to-end GDKP workflow, including coverage-first curricula and broad-domain publications, by validating project state, scheduling the sole owning Skill for each next action, minimizing user interruptions, and reporting verified outcomes. Use to start, resume, reroute, or complete a GDKP project; do not author another Skill's artifacts.
---

# Knowledge Product Orchestrator

Act as the only control plane for a goal-driven knowledge or product project. Keep the workflow recoverable while making the human experience feel like one coherent Codex task rather than a chain of schemas and approval files.

## Required Contracts

Read [workflow-contracts.md](../../references/workflow-contracts.md) before routing any work. Read [curriculum-coverage-policy.md](../../references/curriculum-coverage-policy.md) whenever the request is a textbook, curriculum, comprehensive survey, field-level learning map, or unusually broad knowledge goal. Read [question-gates.md](../../references/question-gates.md) whenever a handoff proposes user input. Read [project-kernel.md](../../references/project-kernel.md) for initialization, binding, recovery, or capability state.

## Core Behavior

1. Resolve or validate ProjectContext through `project-workspace-lifecycle`.
2. Route a new or materially changed goal to `intent-source-analysis` for the compact brief.
3. Inspect the returned CoverageProfile. For ordinary focused work, route the confirmed brief to `requirement-reconstruction`. For `coverage_first` work, route user-approved or user-specified structural sources to `zotero-source-gate` for a CoverageBaseline before requirement reconstruction.
4. Route the confirmed brief and any required CoverageBaseline to `requirement-reconstruction`; accept its internal GoalContract, CoverageContract, and WorkPackageGraph without creating a routine schema review.
5. Route the result to `knowledge-framework`. For coverage-first work, require a current TopicCoverageMatrix, OmissionLedger, and passing CoverageAuditReceipt before presenting or using the framework as complete.
6. Schedule `knowledge-framework`, `zotero-source-gate`, and `notion-node-author` as an internal composition loop until every planned publication unit has a complete substantive draft.
7. Route each complete publication unit through `notion-natural-prose-editor`, then return it to `notion-node-author` to extract the final DraftClaimSet. Route factual claims to `zotero-source-gate`; publish only the audited revision and require persistence-and-reload verification. Keep the global PublicationCoverageIndex current.
8. When a verified Notion revision advances, mark its prior Obsidian projection stale. Route only the verified publication revision to `obsidian-knowledge-views`, and require the intended Vault and native graph settings to be read back before declaring the graph current.
9. Route executable learning or product work to `outcome-orchestrator`.
10. Dispatch reuse, evolution, or domain-Skill acquisition only when their explicit trigger exists.
11. Checkpoint verified results and give the user a concise outcome-first report.

## Interaction Budget

For an ordinary new knowledge project, target no more than:

- one short intake for outcome and source boundary;
- one decision on AI-suggested supplemental sources.

In coverage-first work, the supplemental-source decision may occur before framework design because structural sources are required to establish the field boundary. Reuse that decision for unchanged candidates. A user-requested framework confirmation is an additional reserved decision, not permission to skip the structural baseline.

All other requirement reconstruction, framework decisions, evidence audits, Notion drafting, publication, graph selection, and verification are AI-owned. Do not expose internal artifacts for approval. Ask again only for Q3, Q4, Q5, a material goal ambiguity, or a risky action defined by the question policy.

## Coverage-First Routing

Activate coverage-first routing when the confirmed goal is a textbook, curriculum, comprehensive survey, broad field map, or other unusually large domain whose outline may be treated as a map of what exists.

- Treat breadth and per-topic mastery as independent. A weak learner profile changes sequence and depth, never the visible field boundary by itself.
- Do not interpret `confirm the framework first` as a ban on structural-source work needed to make that framework reliable. Continue to hold factual source admission, prose, graph projection, and outcome execution as requested.
- Use the user's structural sources directly when pre-authorized. Otherwise route one concise structural-source shortlist through `zotero-source-gate`.
- Do not accept `requirements covered`, an internally coherent hierarchy, or a list of source gaps as proof of domain completeness.
- If a CoverageBaseline is unavailable, report `coverage_unverified` and the smallest concrete limitation. Do not substitute confident model-memory enumeration. If an exact authorized local structural document has been hashed, extracted, and read back but Zotero is unavailable, accept `coverage_local_verified` for framework work only and disclose that source admission and factual evidence remain pending.
- When source comparison reveals a material branch omitted by the current goal artifacts, route back to the owning Skill with `needs_replan`; do not repair another owner's contract locally.
- Freeze the verified global framework before large-scale authoring. Schedule bounded publication units and require every included target to reach verified publication or governed omission before declaring the book complete.

## Routing Discipline

- Validate artifact owner, project identity, revision, checksum, binding revision, and required capability before dispatch.
- Validate narrowing authority through the ScopeDecisionLedger and validate coverage-first frameworks with [validate_coverage_audit.py](../../scripts/validate_coverage_audit.py).
- A `next_skill` value is a recommendation to this orchestrator, not authority for one Skill to invoke another.
- Run independent, ready branches in parallel when their writes do not conflict.
- Serialize writes to the same external target or machine artifact.
- Resume from the last verified checkpoint; inspect an operation before retrying it.
- Return stale inputs to their owning Skill with `needs_replan` rather than repairing them here.
- Treat wording, organization, depth, application-path, and reader-experience feedback as a publication revision owned by `notion-node-author`, with `notion-natural-prose-editor` applied before the next final claim audit.
- Re-audit any revision that changes factual meaning, scope, qualification, citation support, or equation semantics. A purely presentational change may reuse an audit only when the canonical fact-bearing draft is unchanged.
- Treat graph density, visual hierarchy, note readability, and navigation feedback as a projection revision owned by `obsidian-knowledge-views`; do not reconstruct the goal unless the requested knowledge scope also changes.
- Never refresh Obsidian from a draft, a pending Notion write, or an unverified publication revision.
- Never use a sparse Obsidian projection as evidence that the complete Notion publication or field framework is sparse.

## Publication and Graph Policy

Notion receives only finished textbook-style knowledge or a requested final product document. It never receives questions, task state, audits, receipts, or workflow commentary. Its equations use native equation objects with strict LaTeX, and completion requires a persisted-page reload with no raw delimiters. Obsidian receives selective student-note synthesis and one sparse semantic graph rendered through native Global Graph and Local Graph views. Do not generate Maps, Canvas files, or a parallel local-view system by default. Before any Obsidian connector write or read, confirm that its active Vault is the bound project Vault; a path mismatch is an unavailable connector, not permission to touch another Vault.

For a large publication, Notion may be authored in coherent verified units while the complete global hierarchy remains fixed and tracked internally. A verified chapter is not a verified book; completion requires the PublicationCoverageIndex to account for every included framework target.

## Scoped Writes

Treat the confirmed project brief as authorization for reversible workflow-owned writes to the bound project collection, publication root, Vault, Kernel, and output paths. Keep the plan, operation ID, read-back, and verification internal. Escalate destructive, ambiguous, costly, credential-sensitive, out-of-scope, or user-content-overwriting actions.

## Completion

Report completion only when the relevant external targets were read back and the declared learning or product acceptance evidence exists. A published chapter is not proof of mastery, and a completed task log is not proof of a working product.

For coverage-first work, also require the latest CoverageAuditReceipt to pass and every included publication target to be verified or explicitly reclassified through the governed omission process. `coverage_local_verified` may complete framework confirmation but cannot by itself complete source admission, factual claim audit, citation readiness, or the final publication. Never describe requirement coverage as domain completeness.

Return a short user summary containing what was produced, where to review it, what was verified, and only the next decision or limitation that genuinely matters.
