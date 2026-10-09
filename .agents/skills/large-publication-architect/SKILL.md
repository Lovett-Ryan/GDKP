---
name: large-publication-architect
description: Produce or revise a complete full-book chapter-to-knowledge map for very large textbooks and monographs, group related knowledge without compressing local depth, and perform one bounded pre-publication semantic review of canonical drafts. Use for explicitly 100k+ publications, multi-unit books, broad weak-foundation learning goals, or requested revisions of incomplete, shallow, or disconnected drafts; do not audit published Notion pages, define domain coverage, admit evidence, publish content, or route the workflow.
---

# Large Publication Architect

Design the semantic and narrative architecture of a large publication. Make the whole book complete enough to drive authoring while keeping its visible structure readable: more knowledge may require more hidden work, but not more artificial headings or thinner explanations.

## Required Contracts

Read [workflow-contracts.md](../../references/workflow-contracts.md) before handoff. Read [large-publication-state-contract.md](../../references/large-publication-state-contract.md) before producing a map, Packet boundary, or DraftQualityReview. Read [project-kernel.md](../../references/project-kernel.md) when resuming from, describing, or validating external checkpoints. Read [curriculum-coverage-policy.md](../../references/curriculum-coverage-policy.md) for a textbook, curriculum, comprehensive survey, field-level learning map, or other `coverage_first` project.

## Inputs and Modes

Require a current ProjectContext, confirmed GoalContract and RequirementContract, the complete user-stated knowledge requirements, and the current FrameworkSpec with its node, relation, and ClaimIntent mappings. For `coverage_first` work, also require the current CoverageContract, TopicCoverageMatrix, OmissionLedger, and passing CoverageAuditReceipt. Do not substitute model-memory enumeration for missing or unverified domain coverage.

Choose one mode:

- **New publication:** build the complete `FullBookChapterKnowledgeMap` before any reader-facing prose is authored.
- **Existing-publication revision:** require a full-book snapshot plus its governing requirements, framework revisions, current map when one exists, and PublicationCoverageIndex. Reconstruct the actual chapter-to-knowledge map before diagnosing it. The snapshot must be supplied by the orchestrator or publication owner; do not call Notion directly.
- **Single-pass draft review:** for `large_publication` work only, inspect one coherent canonical local draft against its assigned knowledge obligations and required relationships immediately before claim extraction and publication. Do not call Notion or review the same draft revision twice.

Reject stale project, requirement, framework, coverage, snapshot, or checkpoint bindings. Return the mismatch to its owner rather than repairing another Skill's artifact.

## Architectural Invariants

Keep these layers distinct:

```text
Framework node != teaching topic != DraftPacket != prose paragraph != visible heading
```

- A Framework node is an internal coverage and traceability unit.
- A teaching topic is a coherent explanation organized around one central question.
- A `DraftPacket` is a hidden, bounded generation and recovery unit.
- Paragraphs perform the explanation.
- Headings exist only when readers need navigation across a real topic or reasoning change.

Global scale changes scheduling, never local depth. When the book grows, increase the number of DraftPackets and model calls; never respond by turning substantive points into keywords, shortening every explanation, or silently omitting detail. Fewer visible headings and more knowledge are compatible because one teaching topic may use several DraftPackets and many continuous paragraphs.

Treat one Architect task as one complete full-book result, not one model inference. Work internally in bounded passes when necessary, checkpoint progress, and continue automatically. Do not return the first chapter as `ready`, wait for the user to say "continue," or make exercises a publication gate. Default to `exercise_gate: false` unless the user explicitly chose an interactive unlock-by-learning mode.

## Build the Full-Book Map

1. Freeze the input revisions and collect every explicit user requirement, confirmed framework target, prerequisite, relation that needs explanation, and governed omission.
2. Turn each included target into a substantive knowledge obligation. State what must be understood: the definition, mechanism, derivation, comparison, constraint, example, boundary, consequence, or connection that matters. A topic name alone is not an obligation.
3. Group related obligations into teaching topics that answer a common central question. Preserve the specific content of merged points; aggregation must not erase detail.
4. Arrange teaching topics into chapters and a full-book progression. Make prerequisites, chapter conclusions, later reuse, and transitions explicit enough for an author to continue the argument rather than restart it.
5. Add hidden DraftPacket boundaries wherever one reliable generation pass would be overloaded. Keep these boundaries out of the reader-facing outline.
6. Reconcile the assembled map against the complete requirement and framework set. Every included knowledge obligation must have a destination; every exclusion or evidence/coverage conflict must be returned explicitly to its owner.
7. Review the complete book as one unit for duplicate introductions, missing bridges, inconsistent terminology, false topic boundaries, and chapters whose title count exceeds their actual knowledge.

Return the map as a real pre-authoring artifact with its complete obligation set and input artifact types. Do not derive it from generated headings, a Packet queue, DraftClaimSet, publication receipt, or completed Notion pages in new-publication mode. For an existing-publication revision, record the supplied snapshot as an input and finish the reconstructed map before replacement prose begins. The orchestrator freezes its revision and SHA-256; Architect never backdates or reconstructs that freeze after authoring.

The human-readable `FullBookChapterKnowledgeMap` is the primary result. It is not a fixed form, but each chapter must make clear:

- the central problem it resolves;
- the substantive knowledge to be explained, in natural language;
- which points form continuous teaching topics and why;
- the order of explanation and the connection to adjacent chapters;
- any missing mechanism, derivation, example, boundary, or application link.

Do not expose Framework IDs as the content, manufacture one heading per knowledge point, or create a new approval gate. Unless the user explicitly reserved framework confirmation, return the complete map to the orchestrator for automatic continuation.

## Aggregate Topics Without Losing Knowledge

Prefer aggregation when points answer the same central question, form a mechanism or causal chain, share prerequisites, occupy one comparison axis, or would repeat context if separated. Prefer a new topic boundary when the central question, object, abstraction level, prerequisite set, or independent reading purpose genuinely changes.

Use three editorial tests:

1. If deleting adjacent headings needs only a natural causal, progressive, or comparative bridge, merge them.
2. If a heading contains only a definition, one equation, or a short statement, it is probably not an independent teaching topic.
3. If merging reveals that the section contains little actual knowledge, deepen the mechanisms, reasoning, examples, boundaries, and connections or honestly reduce the outline. Never restore thin headings to simulate completeness.

For most explanatory material, plan a natural **definition + explanation + role/connection** progression. This is paragraph logic, not three mandatory headings or sentences. Derivations, examples, comparisons, and transitions may use the structure appropriate to their purpose.

## Isolate Scale with DraftPackets

A DraftPacket is normally a bounded part of one teaching topic or argument. It may cover several related Framework nodes, and one teaching topic may require several Packets. Define each Packet from its complete local knowledge obligations, required global narrative anchor, prerequisite or adjacent context, terminology and symbols, and intended bridge to the next Packet. Record an obligation- or argument-based scope rationale and a capacity reservation for input, output, and safety margin. Do not default to one Packet per chapter, page, heading, or connector operation.

If the instructions, global spine, local obligations, evidence context, adjacent prose, output allowance, and safety margin do not fit reliably, split the Packet. Context pressure may cause checkpointing and additional Packets; it must never cause summary-style compression, silent omission, or weaker local acceptance criteria.

Use two context layers without confusing them:

```text
runtime compaction = replaceable conversational working cache
external checkpoint = canonical recovery state
```

Runtime compaction may preserve a concise goal and next-step summary, but it is not a publication store and cannot prove completion. After compaction, restart, or Agent change, recover from the Project Kernel checkpoint supplied by the orchestrator. Validate the bound requirement, map, framework, and evidence revisions; the Packet queue and current status; accepted prose content or stable publication location; Zotero claim-audit and publish-operation states; and the continuity information needed by the next Packet.

Never infer `accepted` from a compaction summary, regenerate accepted prose from a whole-book summary, or continue across a revision/hash mismatch. Mark affected state stale and resume from the last verified checkpoint. Architect may define Packet boundaries and checkpoint needs, but the orchestrator owns persistence, scheduling, recovery, and book-level completion.

## Existing-Publication Revision

Reconstruct the complete book before proposing local edits. Compare the full snapshot with the canonical requirements and map, then identify:

- adjacent headings that fragment one mechanism or reasoning chain;
- user-requested or mapped knowledge that is absent, only named, or materially compressed;
- thin sections with a definition but no explanation, consequence, boundary, or connection;
- repeated setup that should instead deepen or transfer prior knowledge;
- missing bridges that prevent safe aggregation;
- technical publication-unit or DraftPacket boundaries leaked into visible structure.

Return a `NarrativeRevisionMemo` that explains what should be merged, where real expansion is required, and which gaps belong to Framework or evidence owners. Recommend local, bounded revisions; do not request a global summarizing rewrite that could compress already accepted content.

## Traceability Without Node-Shaped Prose

Maintain a minimal hidden relation that prevents obligations from disappearing before authoring:

```text
knowledge point -> requirement anchor -> chapter and teaching topic -> DraftPacket
```

The publication owner records each obligation's scheduled DraftPacket and published page destination in the existing PublicationCoverageIndex. Multiple points may share continuous prose, and one point may span several paragraphs. This lightweight trace does not require a post-write content audit, create headings, prescribe paragraph counts, or become a user-facing checklist.

## Single-Pass Pre-Publication Draft Review

Matrix-scale revision evidence shows that one independent semantic pass can find substantive omissions that source checks cannot: a missing mechanism, derivation, application connection, boundary, or transition may be factually harmless yet educationally important. Preserve that value without rebuilding a recursive audit loop.

For each coherent large-publication unit, review the canonical local draft once after substantive authoring and before final DraftClaimSet extraction. Start only from a `review-ready` state. The review must run in a distinct model execution whose execution ID differs from every Author execution that produced or repaired the unit. A review unit is normally a chapter or other reader-coherent publication unit, never each DraftPacket or each knowledge point. If one unit cannot fit reliably, inspect non-overlapping slices internally and merge them into one review artifact; do not reread the same prose in overlapping passes. Use only the unit's exact assigned obligations, required relationships, target depth, and assembled draft hash. Return a compact `DraftQualityReview` containing only:

- obligations or relationships that are absent, materially under-explained, or incorrectly connected;
- the smallest local repair needed;
- whether the repair can use admitted evidence or requires Zotero source work.

Bind the review to the assembled draft SHA-256, record `review_mode: model_semantic_review`, `basis: semantic_obligations_and_relationships`, the exact obligation IDs, relevant relation IDs, concrete observations, and the smallest repair for every finding. Do not score style, count headings or words, inspect formatting, demand one witness per knowledge point, or reload a published page. A script, regex, metric threshold, or hard-coded empty finding list cannot produce or pass this review. If no substantive issue exists, return `passed`. If issues exist, the Author gets one bounded repair pass. Do not independently review the repaired revision again; any changed factual wording proceeds through the Zotero claim audit, and later concrete user feedback starts a targeted revision rather than another automatic audit. One unit therefore receives at most one Architect draft review in a publication run.

## No Routine Post-Write Audit

After publication, do not reread generated Notion pages, inspect per-point prose witnesses, run semantic-realization checks, or create a second acceptance loop. The scale guarantee combines prospective obligation scheduling with the one bounded pre-publication draft review. Zotero remains the sole source and factual-claim audit owner.

Use the existing-publication revision mode only when the user requests revision or provides concrete feedback about an existing draft. It is an editing task, not an automatic audit after every write.

## Ownership Boundaries

- `knowledge-framework` owns domain coverage, Framework nodes, relations, ClaimIntents, and governed omissions. Architect reorganizes included material for teaching; it does not add a missing field from memory.
- `zotero-source-gate` owns source admission and factual claim support. Architect may expose an evidence need but must not admit a source or invent factual content.
- `notion-node-author` owns prose, visible headings, citations, bounded repairs, Notion writes, and publication results. Architect may review the canonical local draft once but does not call the connector, write publication prose, or audit published pages.
- `knowledge-product-orchestrator` is the sole control plane. Architect returns artifacts and status to it; a suggested next owner is not authority to invoke or schedule another Skill.
- `outcome-orchestrator` owns exercises and mastery evidence. These do not block complete publication unless the user explicitly chose interactive progression.

Do not modify another owner's artifact, publish to Notion, route downstream work, admit evidence, declare domain coverage, or declare the book complete.

## Handoff and Completion

Return to `knowledge-product-orchestrator`:

- the complete `FullBookChapterKnowledgeMap` for a new publication, or the reconstructed map plus `NarrativeRevisionMemo` for a revision;
- when invoked in review mode, one compact `DraftQualityReview` bound to the canonical local draft revision and containing no post-write evidence;
- for every review, its distinct execution ID, assembled draft SHA-256, exact obligation and relationship scope, semantic review mode, and concrete findings or an explicit no-finding result;
- minimal hidden requirement-to-topic traceability and DraftPacket boundary annotations;
- unresolved coverage, evidence, scope, or revision conflicts with the owning Skill identified;
- `ready`, `needs_question`, `needs_replan`, or `blocked` as appropriate.

Use `ready` when the entire requested book is represented, explicit user knowledge has no silent disappearance, teaching-topic aggregation preserves local depth, DraftPacket boundaries can isolate context pressure, and all input revisions remain current. A complete map is ready for orchestration, but is not evidence that prose was authored, published, or learned.
