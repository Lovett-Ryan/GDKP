# Curriculum and Broad-Domain Coverage

Use this policy when a learning goal or publication is expected to represent a field rather than answer one focused question. It prevents learner adaptation, time pressure, or model recall limits from silently deleting parts of the subject.

## Coverage-First Trigger

Enter `coverage_first` mode when any of the following materially applies:

- the requested product is a textbook, monograph, handbook, curriculum, course, or comprehensive survey;
- the topic is field-level or has an unusually large and uncertain boundary;
- the user asks for comprehensive, systematic, complete, broad, end-to-end, or reference-style coverage;
- a learner is likely to treat the resulting outline as a map of what exists in the field.

A focused chapter, narrow question, local product, or explicitly bounded tutorial does not require this mode. When the trigger is ambiguous and the choice would materially change scope, ask one concise question.

## Separate Breadth From Depth

Record coverage breadth and learning depth as independent decisions.

Coverage breadth may be focused, canonical foundations, broad field map, or reference-comprehensive. Learning depth is assigned per topic as awareness, understanding, or mastery. A weak foundation may change order, scaffolding, notation load, examples, and initial depth; it must not silently reduce the visible breadth of the field.

The following implications are invalid unless the user explicitly confirms them:

- `not required for mastery` therefore `absent from the outline`;
- `selected foundational models` therefore `other major model families do not need to be named`;
- `beginner` therefore `only a minimal topic set`;
- `not exhaustive of every paper or implementation` therefore `major canonical branches may be omitted`.

## Scope Decision Provenance

`intent-source-analysis` owns a revisioned ScopeDecisionLedger. For every material normalization, it records:

- the raw user fragment and anchor;
- the normalized clause;
- whether the transformation preserves, expands, narrows, excludes, or infers scope;
- the authority: explicit user statement, governing policy, admitted structural evidence, or AI judgment;
- confidence, question state, and affected downstream artifacts.

A narrowing or exclusion requires explicit user authority or a named governing policy. AI judgment alone may propose a narrowing but may not confirm it. If the material choice is unresolved, return `needs_question`. Downstream Skills must reject a narrowing whose authority cannot be traced through the ledger.

## Structural Sources

Structural sources establish what topics and relationships a curriculum should consider. They are distinct from factual evidence used to support publication claims.

Suitable structural sources include authoritative textbook tables of contents, recognized course syllabi, standards or competency frameworks, and high-quality surveys or taxonomies. Prefer multiple independent sources when one source may reflect a narrow school, application, era, or author preference. A single user-selected source may be used as the instructional spine, but its known boundary must remain visible.

`zotero-source-gate` owns the CoverageBaseline. It records source role, identity, version or date, independence, authority, scope, extracted topics and aliases, topic prominence, dependencies, disagreements, and known blind spots. Structural metadata or a table of contents may guide framework coverage, but it is not evidence for the factual claims inside a chapter.

AI-suggested structural sources use the ordinary one-time supplemental shortlist decision. User-specified structural sources acknowledged during intake are pre-authorized. Inspection is not admission: unavailable or unapproved candidates may inform a shortlist but may not be represented as an admitted baseline.

When Zotero is temporarily unavailable, an exact user-specified or user-approved local document may produce a degraded but auditable CoverageBaseline with status `local_files_verified`. Record its resolved location, lowercase SHA-256 content digest, extraction method, read-back verification, and user-authorization anchor. A passing framework audit based on that baseline uses `coverage_local_verified`, not `coverage_verified`. It may support framework comparison and confirmation, but it does not admit the document as factual claim evidence or authorize publication citations. Proposed, inaccessible, unhashed, or model-recalled sources remain `coverage_unverified`.

## Coverage Contract

`requirement-reconstruction` owns the CoverageContract for a `coverage_first` project. It combines confirmed intent with the current CoverageBaseline and records:

- breadth profile and the meaning of completeness for this project;
- required topic classes and depth-allocation rules;
- audience and prerequisite policy;
- source and recency boundaries;
- allowed exclusions and their authority;
- coverage acceptance tests and invalidation conditions.

Requirement coverage and domain coverage are different states. `requirements_coverage_complete` means all confirmed requirements are mapped. It must never be reported as `domain_coverage_complete` or `coverage_verified` without a passing external coverage audit.

## Framework Coverage Artifacts

For `coverage_first` work, `knowledge-framework` additionally owns:

- TopicCoverageMatrix: maps every baseline topic to mastery, understanding, awareness, deferred, or excluded;
- OmissionLedger: explains every deferred or excluded topic, authority, learner impact, and future route;
- CoverageAuditReceipt: binds the CoverageContract, CoverageBaseline, framework revision, matrix, omissions, and deterministic validation result.

Every baseline topic must have exactly one disposition. Mastery, understanding, and awareness require a concrete framework target. Deferred and excluded topics require an OmissionLedger entry. A core topic may not be excluded solely to reduce length, simplify a beginner curriculum, or fit one model turn.

Run [validate_coverage_audit.py](../scripts/validate_coverage_audit.py) on the assembled coverage audit. Without a current CoverageBaseline and passing audit, the framework returns `needs_sources` or `coverage_unverified`; it does not claim completeness. A passing `local_files_verified` baseline permits `coverage_local_verified` only, with its Zotero and factual-evidence limitation kept visible.

## Dependency Closure

The framework must expose the prerequisites needed to understand every mastery or understanding topic. A prerequisite may be taught just in time or placed in a reference appendix, but it may not disappear. When a prerequisite is intentionally deferred, state the resulting limit on downstream understanding.

## Orthogonal Large-Publication Branch

`coverage_first` and large-publication execution solve different problems:

- `coverage_first` governs field boundary, topic inclusion, depth disposition, omissions, and prerequisite closure;
- large-publication execution governs the complete chapter-to-knowledge plan, semantic grouping, bounded authoring, context recovery, and prospective assignment of every planned obligation to a publication unit.

Apply each branch from its own trigger. A broad map may need coverage verification without a long publication, while a large revision of an already bounded publication may need scale isolation without reopening its confirmed field boundary. When both apply, coverage is verified first and its artifacts constrain the large-publication plan; the large-publication branch may reorganize exposition but may not silently add, remove, defer, or reclassify framework scope. Conversely, coverage status cannot be used as evidence that the prose is coherent, sufficiently detailed, or fully published.

## Large-Publication Execution

After the applicable requirements and framework scope are current, `large-publication-architect` owns one complete, human-readable `FullBookChapterKnowledgeMap` before new or revised Notion authoring begins. It maps every chapter to substantive knowledge points, groups related points into teaching topics, preserves the specific content of confirmed user requirements, and states the intended narrative order. It is an atomic full-book result: internal checkpointing is allowed, but the first chapter, a representative sample, or a partial map may not be returned as ready merely because one model turn is full. The map is not a replacement for FrameworkSpec, TopicCoverageMatrix, OmissionLedger, EvidencePack, or PublicationCoverageIndex and cannot mutate their owners' decisions.

Keep these granularities separate:

```text
framework target
-> substantive knowledge point
-> teaching topic
-> one or more hidden DraftPackets
-> continuous paragraphs
-> reader-visible headings only where navigation requires them
```

A substantive knowledge point is an exposition obligation, not a keyword or a heading. It must say what concept, mechanism, relationship, derivation, boundary, or application the prose needs to explain. Several points may be fulfilled by one continuous passage, and one complex point may span multiple DraftPackets. Removing headings never authorizes removing their knowledge obligations.

`knowledge-product-orchestrator` persists the canonical map revision and schedules the full DraftPacket queue. Each Packet receives only the global narrative spine, its complete local knowledge obligations, admitted local evidence, required terminology and notation, relevant adjacent accepted prose, and the next-step intent. If that material cannot fit with enough output capacity, split the Packet and continue automatically; do not shorten the obligations, turn them into an overview, omit details, expose the technical split as extra headings, or ask the user to reply `continue`.

Runtime compaction and external checkpoints operate together. Compaction keeps a long control conversation usable, but it is not publication state. Each DraftPacket checkpoint must live in Project Kernel state or a referenced versioned artifact and bind the requirement, map, framework, evidence, and publication revisions; Packet obligations and status; accepted draft content or stable page destination; continuity context; the single-pass DraftQualityReview state; Zotero claim-audit state; and publication-operation state. After compaction, restart, or agent transfer, recover from this checkpoint rather than model memory. A mismatch invalidates affected states, and accepted prose must not be regenerated from a conversation summary.

`notion-node-author` continues to own PublicationCoverageIndex and the published prose. The index is a lightweight prospective trace from each included framework target and substantive knowledge point through the canonical map to its DraftPacket and intended page. It prevents obligations from disappearing during scheduling without creating visible headings or one paragraph per point. Before final claim extraction, each coherent large-publication unit receives one bounded Architect DraftQualityReview against its assigned obligations and relationships; findings receive one Author repair pass or are routed to their source/scope owner, with no Architect re-review. Zotero then owns source admission and factual-claim audit. Notion prose is not reloaded for semantic, style, block, equation, citation-count, or hierarchy review, and Obsidian projections are not reread for graph review. Concrete user feedback can trigger a targeted revision.

Large size changes scheduling, not coverage:

- keep the complete canonical chapter-to-knowledge map recoverable and expose its natural-language full-book view to the user without making it a routine approval gate;
- author and publish bounded DraftPackets and coherent publication units incrementally while preserving local depth;
- serialize writes to the same external publication target;
- re-run the coverage audit after a material framework revision;
- continue automatically after the first successful Packet, chapter, or publication-unit smoke test;
- keep `exercise_gate: false` unless the user explicitly chooses an interactive, staged-release course;
- declare the publication complete only when the full-book completion barrier passes.

The full-book completion barrier requires all of the following:

1. the canonical `FullBookChapterKnowledgeMap` is complete and bound to current upstream revisions;
2. every included framework target, substantive knowledge point, and required relationship is assigned to a completed DraftPacket and intended published page, or is explicitly reclassified through the owning governed process;
3. the DraftPacket queue contains no pending, partial, stale, or silently omitted work;
4. each coherent publication unit has exactly one completed DraftQualityReview with every finding repaired once or governed, the final factual revision has a current Zotero claim audit, and every publication unit has a successful write result tied to its intended native target;
5. no technical batch boundary remains as an accidental reader-facing structure;
6. no learner exercise, experiment, response, or mastery result is being used as a substitute for publication evidence.

Publication construction and learner validation are independent progress tracks. The default workflow finishes the complete publication before `outcome-orchestrator` takes over the main path for exercises or mastery evidence. Exercises may be prepared earlier as a non-blocking side branch, but incomplete learner work cannot pause the remaining chapters. Only an explicit interactive-course choice may make learner progress affect release order, and that choice does not weaken the full-book completion criteria for the publication eventually promised.

## Completion Standard

A curriculum or broad-domain framework is coverage-verified, or locally coverage-verified under the degraded rule above, only when:

1. the breadth and per-topic depth policy are confirmed;
2. the CoverageBaseline is current and source-bounded;
3. every baseline topic is represented or governed by an omission;
4. prerequisite closure is checked;
5. source disagreements and unresolved blind spots remain visible internally;
6. the deterministic coverage audit passes.

Coverage verification does not mean every possible paper, implementation, application, or historical detail is included. It means the chosen field boundary is externally grounded and no major topic inside that boundary disappeared without an accountable decision.

Coverage verification, full-book publication completion, and learner mastery are three independent claims. Report each from its own evidence; never infer one from another.
