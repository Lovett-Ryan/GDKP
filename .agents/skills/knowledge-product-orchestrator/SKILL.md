---
name: knowledge-product-orchestrator
description: Coordinate the end-to-end GDKP workflow, including coverage-first curricula and scale-isolated large publications, by validating project state, scheduling the sole owning Skill for each next action, minimizing user interruptions, and reporting verified outcomes. Use to start, resume, reroute, or complete a GDKP project; do not author another Skill's artifacts.
---

# Knowledge Product Orchestrator

Act as the only control plane for a goal-driven knowledge or product project. Keep the workflow recoverable while making the human experience feel like one coherent Codex task rather than a chain of schemas and approval files.

## Required Contracts

Read [workflow-contracts.md](../../references/workflow-contracts.md) before routing any work. Read [curriculum-coverage-policy.md](../../references/curriculum-coverage-policy.md) whenever the request is a textbook, curriculum, comprehensive survey, field-level learning map, or unusually broad knowledge goal. Read [large-publication-state-contract.md](../../references/large-publication-state-contract.md) before starting, resuming, or completing any `large_publication` run. Read [question-gates.md](../../references/question-gates.md) whenever a handoff proposes user input. Read [project-kernel.md](../../references/project-kernel.md) for initialization, binding, recovery, or capability state.

## Core Behavior

1. Resolve or validate ProjectContext through `project-workspace-lifecycle`.
2. Route a new or materially changed goal to `intent-source-analysis` for the compact brief.
3. Inspect the returned CoverageProfile. For ordinary focused work, route the confirmed brief to `requirement-reconstruction`. For `coverage_first` work, route user-approved or user-specified structural sources to `zotero-source-gate` for a CoverageBaseline before requirement reconstruction.
4. Route the confirmed brief and any required CoverageBaseline to `requirement-reconstruction`; accept its internal GoalContract, CoverageContract, and WorkPackageGraph without creating a routine schema review.
5. Route the result to `knowledge-framework`. For coverage-first work, require a current TopicCoverageMatrix, OmissionLedger, and passing CoverageAuditReceipt before presenting or using the framework as complete.
6. Inspect the confirmed `large_publication` signal independently from `coverage_first`. When active, route the complete current requirements and framework to `large-publication-architect`; require one complete `FullBookChapterKnowledgeMap` before new reader-facing authoring begins. Create `LargePublicationRunState`, freeze the map hash and complete obligation set, then pass the `map-ready` gate before the first Author dispatch. Invoke existing-publication revision mode only for explicit user feedback or a requested revision, never as a routine post-write audit.
7. Compile hidden DraftPacket boundaries prospectively into the durable state. Before every Author call, pass `packet-dispatch`; after the call, persist the actual draft and checkpoint and pass `packet-checkpoint` before dispatching a dependent Packet. One Packet has one dispatch and one Author execution ID. A chapter, page, or heading boundary alone cannot justify Packet scope. For ordinary work, keep the existing bounded composition loop without large-publication state.
8. Assemble only accepted Packets. Pass `review-ready`, then route each coherent canonical local draft once to `large-publication-architect` in a distinct execution for a bounded pre-publication `DraftQualityReview`. Immediately persist the result and pass `review-recorded`. If it identifies a substantive omission or broken relationship, allow one local Author repair or route a real evidence gap to Zotero; never send the repaired draft through a second Architect review.
9. Pass `claim-audit-ready`, let `notion-node-author` extract the final DraftClaimSet, and route it with the exact EvidencePack to `zotero-source-gate`, the sole source and factual-claim audit owner. Validate the receipt with `validate_claim_audit.py --evidence-pack`; identifier equality alone cannot pass. Return the passing receipt and citation-ready source metadata to Notion Author, require a `CitationProjection` bound to the audited fact draft, and validate it with `validate_citation_projection.py` before `publish-ready`. Then publish the projected draft once and record connector-returned page identities without Notion reload, reread, post-write semantic review, block checks, or a second acceptance loop.
10. Route the published NotionPublicationPack to `obsidian-knowledge-views` for one direct projection pass. Accept successful scoped write results without rereading notes, recounting graph elements, resolving every link, or auditing native graph settings.
11. Route executable learning or product work to `outcome-orchestrator`. For a large publication, do not let exercises or mastery validation take over the main path before the full-book publication barrier passes unless the user explicitly selected an interactive chapter-unlock course.
12. Dispatch reuse, evolution, or domain-Skill acquisition only when their explicit trigger exists.
13. Checkpoint completed work and give the user a concise outcome-first report.

## Interaction Budget

For an ordinary new knowledge project, target no more than:

- one short intake for outcome and source boundary;
- one decision on AI-suggested supplemental sources.

In coverage-first work, the supplemental-source decision may occur before framework design because structural sources are required to establish the field boundary. Reuse that decision for unchanged candidates. A user-requested framework confirmation is an additional reserved decision, not permission to skip the structural baseline.

All other requirement reconstruction, framework decisions, Zotero source audits, Notion drafting, publication, and graph selection are AI-owned. Do not expose internal artifacts for approval. Ask again only for Q3, Q4, Q5, a material goal ambiguity, or a risky action defined by the question policy.

A complete `FullBookChapterKnowledgeMap` is normally a user-visible design result but not a new approval gate. Present it when useful, then continue automatically unless the user explicitly reserved full-book-map confirmation.

## Coverage-First Routing

Activate coverage-first routing when the confirmed goal is a textbook, curriculum, comprehensive survey, broad field map, or other unusually large domain whose outline may be treated as a map of what exists.

- Treat breadth and per-topic mastery as independent. A weak learner profile changes sequence and depth, never the visible field boundary by itself.
- Do not interpret `confirm the framework first` as a ban on structural-source work needed to make that framework reliable. Continue to hold factual source admission, prose, graph projection, and outcome execution as requested.
- Use the user's structural sources directly when pre-authorized. Otherwise route one concise structural-source shortlist through `zotero-source-gate`.
- Do not accept `requirements covered`, an internally coherent hierarchy, or a list of source gaps as proof of domain completeness.
- If a CoverageBaseline is unavailable, report `coverage_unverified` and the smallest concrete limitation. Do not substitute confident model-memory enumeration. If an exact authorized local structural document has been hashed, extracted, and read back but Zotero is unavailable, accept `coverage_local_verified` for framework work only and disclose that source admission and factual evidence remain pending.
- When source comparison reveals a material branch omitted by the current goal artifacts, route back to the owning Skill with `needs_replan`; do not repair another owner's contract locally.
- Freeze the coverage-audited global framework before large-scale authoring. Schedule bounded publication units and require every included target to reach a completed source-audited publication unit or governed omission before declaring the book complete.

## Proportional Audit Path

Retain only checks with distinct decision value:

- the deterministic CoverageAudit for broad-domain scope completeness;
- Zotero source admission and exact factual-claim audit for evidential correctness;
- one bounded Architect `DraftQualityReview` before publication for each coherent large-publication unit.

The Architect review checks only substantive realization of assigned obligations and relationships in the canonical local draft. It is neither a source audit nor a style pass, and it may not recurse after repair. CitationProjection validation is a deterministic pre-publication compilation check, not a model review or a post-write citation audit. Do not add a Notion publication reload audit, post-write semantic audit, style audit, block audit, citation-count audit, or Obsidian graph/read-back audit. Connector target resolution and operation results are minimal safety and write-status checks, not content-audit phases.

Do not confuse publication audit reduction with unrelated controls. `domain-skill-acquisition` still performs its security and provenance audit when installing executable third-party guidance, and `outcome-orchestrator` still verifies learning or product acceptance evidence. These protect different risks and do not reread Notion or Obsidian content.

Build quality into the inputs: complete requirements, an evidence-ready framework, admitted evidence, and for large work a complete full-book map plus bounded DraftPackets. The single draft review is a final pre-publication exception detector, not permission to weaken those inputs. If the user later reports a content or graph problem, route a targeted revision from that feedback rather than auditing every successful write preemptively.

## Large-Publication Routing

Activate this branch for an explicitly very large textbook or monograph, a work that needs several reliable drafting units, or a large draft whose requested knowledge is incomplete, shallow, or disconnected. Publication scale and field breadth are orthogonal; run this branch with or without `coverage_first` as the confirmed goal requires.

- Require `large-publication-architect` to preserve the complete user-detail set in a natural-language `FullBookChapterKnowledgeMap`, aggregate related nodes into teaching topics, and annotate hidden DraftPacket boundaries. Do not accept the first chapter, a sample, or a title-only outline as ready.
- Treat `LargePublicationRunState` as the sole forward-state authority. Run [validate_large_publication_state.py](../../scripts/validate_large_publication_state.py) at every prospective gate and append its state-bound hash-chained `gate_receipt` to both the run state and Kernel events before dispatching the next owner. Never create the map, Packet queue, checkpoint, review, audit, or gate receipt retrospectively from headings or published pages.
- Keep Framework nodes, substantive knowledge points, teaching topics, DraftPackets, paragraphs, and visible headings distinct. Heading count never determines Packet count or completion.
- Treat global scale as a scheduling multiplier. More knowledge creates more Packets and model calls; it never lowers a Packet's local explanation obligations.
- Give each worker only the global narrative spine, current complete local obligations, admitted evidence, terminology and notation, relevant adjacent accepted prose, and next-step intent. If the reliable context or output allowance is insufficient, split the Packet; never summarize obligations away.
- Serialize writes to the same Notion target, but run independent evidence or draft preparation in parallel when their dependencies and shared terminology permit it.
- Continue automatically after a successful first Packet, chapter, or connector smoke test. Never ask the user to reply `continue` for already-authorized remaining chapters.

Persist the DraftPacket queue and checkpoint outside model context. Runtime compaction is a replaceable conversation cache. On compaction, restart, or Agent change, reload the canonical map revision, queue, accepted draft content or stable publication destinations, single-pass draft-review state, Zotero claim-audit state, publish-operation state, continuity capsule, and next Packet from Project Kernel. A summary cannot advance a Packet state or regenerate accepted prose. Revision drift invalidates the affected review, Zotero audit, and pending publication state, but does not trigger a Notion or Obsidian reread. A changed draft may receive one review in its new publication run; a repair prompted by that review does not.

## Routing Discipline

- Validate artifact owner, project identity, revision, checksum, binding revision, and required capability before dispatch.
- Validate narrowing authority through the ScopeDecisionLedger and validate coverage-first frameworks with [validate_coverage_audit.py](../../scripts/validate_coverage_audit.py).
- A `next_skill` value is a recommendation to this orchestrator, not authority for one Skill to invoke another.
- Run independent, ready branches in parallel when their writes do not conflict.
- Serialize writes to the same external target or machine artifact.
- Resume from the last verified checkpoint; inspect an operation before retrying it.
- For large publications, validate the checkpoint's requirement, map, framework, evidence, body, and binding revisions before dispatch. Context pressure causes `needs_split` or another internal pass, never content compression or user-facing continuation approval.
- Do not accept a deterministic program as the producer of `DraftQualityReview`. The validator may verify chronology, hashes, role separation, and coverage; only a distinct Architect model execution may judge whether obligations and relationships are substantively realized.
- Return stale inputs to their owning Skill with `needs_replan` rather than repairing them here.
- Treat wording, organization, depth, application-path, and reader-experience feedback as a targeted publication revision owned by `notion-node-author`; use `notion-natural-prose-editor` only when that feedback is about prose quality.
- Re-audit any revision that changes factual meaning, scope, qualification, citation support, or equation semantics. A purely presentational change may reuse an audit only when the canonical fact-bearing draft is unchanged.
- Rebuild and revalidate CitationProjection after any citation number, bibliography, link-label, or original-URL change. Such a presentation-only repair does not consume another Architect review or Zotero claim audit when the fact-bearing draft hash is unchanged.
- Treat graph density, visual hierarchy, note readability, and navigation feedback as a projection revision owned by `obsidian-knowledge-views`; do not reconstruct the goal unless the requested knowledge scope also changes.
- Never refresh Obsidian from a draft or a failed or pending Notion write; use the source-audited publication pack returned by the successful write.
- Never use a sparse Obsidian projection as evidence that the complete Notion publication or field framework is sparse.

## Publication and Graph Policy

Notion receives only finished textbook-style knowledge or a requested final product document. It never receives questions, task state, audits, receipts, or workflow commentary. Its source-audited draft uses strict LaTeX and native equation objects when supported, but the workflow does not reload the page to audit rendering. Obsidian receives selective student-note synthesis and one sparse semantic graph rendered through native Global Graph and Local Graph views. Do not generate Maps, Canvas files, or a parallel local-view system by default. Before an Obsidian connector write, confirm that its active Vault is the bound project Vault; a path mismatch is an unavailable connector, not permission to touch another Vault. Do not read the Vault afterward solely to audit the write.

For a large publication, Notion may be authored in coherent units while the complete global hierarchy and `FullBookChapterKnowledgeMap` remain fixed and tracked internally. Multiple hidden DraftPackets may contribute continuous prose under one natural heading. A published chapter is not a published book; completion requires the queue and lightweight PublicationCoverageIndex to account prospectively for every included framework target and substantive knowledge point.

## Scoped Writes

Treat the confirmed project brief as authorization for reversible workflow-owned writes to the bound project collection, publication root, Vault, Kernel, and output paths. Keep the plan and operation ID internal; record the write result without launching a content read-back audit. Escalate destructive, ambiguous, costly, credential-sensitive, out-of-scope, or user-content-overwriting actions.

## Completion

Report publication completion when all scheduled units have successful write results and no dependent work remains. Learning or product completion still requires its own declared acceptance evidence; a published chapter is not proof of mastery, and a completed task log is not proof of a working product.

For coverage-first work, also require the latest CoverageAuditReceipt to pass and every included publication target to be scheduled and published or explicitly reclassified through the governed omission process. `coverage_local_verified` may complete framework confirmation but cannot by itself complete Zotero source admission, factual claim audit, citation readiness, or publication. Never describe requirement coverage as domain completeness.

For large-publication work, require the `complete` gate of `validate_large_publication_state.py`. Completion means the canonical full-book map was frozen before authoring, every included obligation is assigned to an accepted checkpointed Packet, the queue has no pending or stale work, every coherent unit has exactly one independent pre-publication DraftQualityReview with each finding resolved once, all final factual wording has a current locator-specific Zotero claim audit, every audited unit has a passing CitationProjection, and every required publication unit has a successful write result bound to the projected draft hash. Do not add a second Architect review, post-write semantic review, reload, prose-location, or graph audit. The first completed chapter or learner exercise status cannot satisfy this barrier.

Return a short user summary containing what was produced, where to review it, what was verified, and only the next decision or limitation that genuinely matters.
