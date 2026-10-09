# Workflow Contracts

This is the canonical coordination contract for GDKP v1.1.0. It separates durable machine state from the material a person is expected to read.

## Product Model

Codex is the control plane. It interprets the goal, schedules the owning Skills, keeps resumable state, and reports only decisions or results that matter to the user.

| Surface | v1.1.0 role | Must not become |
|---|---|---|
| Local project | Project identity, machine state, executable work, and deliverables | A folder full of routine approval documents |
| Zotero | Project evidence gate and source registry | A general note-taking or task system |
| Notion | Formal, dense, reader-facing textbook or requested product publication | A workflow console, audit log, chat transcript, or schema viewer |
| Obsidian | Selective student-note synthesis and a cautious relationship graph | A copy of Notion or a second textbook |
| Codex UI | Questions, concise decisions, progress, and outcome reporting | A renderer for internal YAML or JSON |

## Human Interaction Boundary

Machine artifacts may remain structured under `.knowledge-product/` for recovery, validation, and traceability. Never require the user to open or review those artifacts. In particular, do not present nested YAML, JSON, handoff envelopes, receipts, preview files, or schema-oriented Markdown as an approval surface.

When a decision is required:

1. ask in the Codex UI;
2. prefer the host's structured Question mechanism when available;
3. otherwise ask a direct, short question at the end of the turn;
4. present ordinary Markdown prose or a shallow list;
5. state what will change and the meaningful trade-off;
6. record the normalized answer internally without exposing the record unless requested.

Only a project-status diagnostic may use nested structured data in a user-facing response, and only when that representation materially improves diagnosis.

## Default Flow

The normal knowledge flow has two user-facing decision moments at most:

1. a short intake that confirms the outcome and source boundary;
2. one source-shortlist decision for AI-suggested supplemental sources.

User-specified sources are acknowledged during intake and are pre-authorized for project registration. After those decisions, Codex autonomously reconstructs requirements, designs the framework, admits evidence, and writes a complete draft. A coherent large-publication unit receives one bounded Architect semantic review before final claim extraction; ordinary focused publications skip it unless explicitly requested. The final fact-bearing wording then receives the Zotero claim audit, is published once to Notion, and is projected once to Obsidian. The natural-prose editor runs only for an explicit polishing request or concrete prose feedback. Notion and Obsidian do not receive routine post-write content audits or read-back passes; their actual user-facing surfaces collect any later feedback.

Textbooks, curricula, comprehensive surveys, field-level learning maps, and other unusually broad knowledge goals use the coverage-first branch defined in [curriculum-coverage-policy.md](curriculum-coverage-policy.md). In that branch, breadth and per-topic depth are confirmed separately, structural sources establish a CoverageBaseline before final framework design, and a passing coverage audit is required before the framework may be described as complete. Structural discovery may precede framework confirmation; it is not publication authoring or factual claim admission. When Zotero is unavailable, a hashed and read-back user-authorized local structural document may yield `coverage_local_verified` for framework work, but it cannot be promoted to factual evidence or final publication readiness without normal admission.

Coverage-first and large-publication execution are orthogonal. Coverage-first establishes what belongs inside the governed field boundary; `large-publication-architect` determines how an already confirmed large body of knowledge becomes a complete chapter-to-knowledge map and coherent exposition without projecting every framework node into a heading. A project may use either branch or both. A passing coverage audit does not prove that a large publication has sufficient exposition, and a complete `FullBookChapterKnowledgeMap` does not establish domain coverage or admit factual evidence. Large-publication execution follows the forward-only gates in [large-publication-state-contract.md](large-publication-state-contract.md); those gates enforce chronology and bindings without restoring Notion or Obsidian read-back audits.

```text
setup
-> brief_confirmed
-> sources_confirmed
-> composing
-> published
-> graph_stale
-> graph_updated
-> executing
-> completed
```

```text
coverage_first setup
-> brief_confirmed
-> structural_sources_confirmed
-> coverage_baselined
-> requirements_reconstructed
-> framework_coverage_verified
-> framework_confirmed when the user reserved that decision
-> sources_confirmed
-> composing in bounded publication units
-> published
-> graph_updated
-> executing
-> completed
```

Stages are machine checkpoints, not mandatory user approvals. A product-only project may move from `sources_confirmed` to `executing` when no Notion publication or Obsidian graph is required.

## Conditional Decisions

The following decisions remain explicit because they change scope, provenance, or an existing knowledge base:

- Q3: reuse an existing knowledge base;
- Q4: update an existing knowledge base with current-project knowledge;
- Q5: download and install a GitHub Skill;
- a destructive, irreversible, costly, credentialed, out-of-scope, or user-content-overwriting action;
- an ambiguity that would materially change the goal, source boundary, acceptance test, or user/AI responsibility.

Do not invent routine approvals for requirements, framework shape, Notion drafts, graph plans, Zotero item-by-item imports, or reversible in-scope writes.

## Ownership

| Concern or artifact | Sole owner | Primary consumers |
|---|---|---|
| ProjectContext, bindings, capability state | `project-workspace-lifecycle` | All core Skills |
| IntentContract, SourcePolicy, CoverageProfile, ScopeDecisionLedger | `intent-source-analysis` | Requirements, sources, outcomes |
| RequirementContract, GoalContract, WorkPackageGraph, CoverageContract | `requirement-reconstruction` | Framework, outcomes |
| FrameworkSpec, node and relation registries, ClaimIntents, TopicCoverageMatrix, OmissionLedger, CoverageAuditReceipt | `knowledge-framework` | Zotero, Notion, Obsidian |
| FullBookChapterKnowledgeMap, NarrativeRevisionMemo, and single-pass DraftQualityReview | `large-publication-architect` | Orchestrator and Notion Author |
| CandidateManifest, CoverageBaseline, EvidencePack, SourceAuditReport, ClaimAuditReceipt | `zotero-source-gate` | Requirements, framework, Notion, outcomes |
| NaturalProseRevisionMemo | `notion-natural-prose-editor` | Notion Author |
| DraftClaimSet, PublicationCoverageIndex, and NotionPublicationPack | `notion-node-author` | Zotero, Obsidian |
| GraphPlan and KnowledgeGraphManifest | `obsidian-knowledge-views` | Outcomes, evolution |
| ReuseLineage and Q3 | `knowledge-base-reuse` | Requirements, framework |
| EvolutionChangeSet and Q4 | `knowledge-base-evolution` | Core owners through Codex |
| TaskSpec, TaskGraph, OutcomeEvidence | `outcome-orchestrator` | Codex and local executors |
| DomainSkillCandidateManifest, lock entry, receipt, and Q5 | `domain-skill-acquisition` | Lifecycle and Codex |
| LargePublicationRunState, DraftPacket queue, external checkpoint bindings, and full-book completion barrier | `knowledge-product-orchestrator` | Large Publication Architect, Notion Author, prose editor, and source gate |

One Skill may request another owner's work but may not take ownership of it. Every core Skill returns control to `knowledge-product-orchestrator`.

## Evidence and Publication Invariants

1. Factual Notion publication content must be supported by admitted Zotero evidence and an internal claim audit.
2. Requirement coverage and domain coverage are different claims. A broad-domain framework is not coverage-verified without a current CoverageBaseline, one disposition for every baseline topic, governed omissions, prerequisite closure, and a passing coverage audit.
3. Learner adaptation changes sequence, scaffolding, notation load, examples, and depth. It never silently removes major topics from a requested broad field map.
4. Structural sources establish curriculum coverage only. A table of contents, syllabus, taxonomy, or survey outline does not by itself support the factual claims inside a publication.
5. Claim audits are quality controls, not user approval gates.
6. Notion uses natural titles and editorial prose. Stable IDs, revisions, evidence hashes, and audit receipts remain hidden in Project Kernel state or connector properties.
7. Notion drafts use strict LaTeX and native equation objects when supported. Do not reload the published page to audit section continuity, rendering, citations, or References; correct concrete problems only when the connector reports an error or the user identifies one.
8. After the Zotero claim audit, Notion Author compiles a deterministic CitationProjection from audited source identities to contiguous reader-facing numbers and validates it before publication. Notion references contain a formatted citation and a clickable original URL when one exists. They never expose Zotero keys, EvidenceUnit IDs, locators, claim IDs, Source View images, screenshots, thumbnails, bookmarks, iframes, or other previews.
9. Obsidian may paraphrase and reorganize only published, source-audited Notion content as study notes, and it must not introduce unsupported facts.
10. An Obsidian graph contains concrete, meaningful concepts and defensible semantic links. Containers, fields, courses, sources, tasks, and metadata are not graph nodes. It may contain isolated nodes or disconnected components; connectedness is never forced.
11. The default Obsidian output is one semantic graph rendered by native Global Graph and Local Graph views. Maps, Canvas files, screenshots, and manually duplicated local graphs are opt-in artifacts, not default output.
12. A newly published Notion revision makes its earlier Obsidian projection outdated until the current projection write succeeds. Do not reread the Vault merely to audit that projection.
13. Product completion requires a verified deliverable and acceptance evidence. Knowledge completion requires evidence that the learner can use the knowledge, not merely that content was collected.
14. A GitHub-acquired Skill is an execution dependency, never factual evidence or a second control plane.
15. Framework nodes, substantive knowledge points, teaching topics, DraftPackets, paragraphs, and visible headings are distinct granularities. No one-to-one projection among them may be inferred.
16. In large-publication work, scale may increase DraftPacket count and model calls, but it must not silently reduce local exposition depth. Insufficient context triggers a smaller Packet, not summary-style compression, omission, or an extra visible heading.
17. Publication completion and learner mastery are separate states. Exercises, experiments, and learner responses do not gate the remaining publication by default; an exercise gate is allowed only when the user explicitly chooses an interactive, staged-release course.
18. Retain three non-duplicative publication controls: deterministic coverage audit for broad-domain scope, Zotero source and factual-claim audit, and one bounded pre-publication Architect DraftQualityReview for each coherent large-publication unit. A DraftQualityReview may cause one repair pass but never a second Architect review in the same publication run. Notion is not reloaded or semantically audited after a successful write, and Obsidian notes, links, counts, and graph settings are not reread or audited after a successful scoped write. Third-party Skill security/provenance audit and learning/product acceptance verification remain separate controls for separate risks.
19. `LargePublicationRunState` advances only through prospective gates. Freeze the map and obligation set before Author dispatch; checkpoint one Packet before any dependent dispatch; assemble only accepted Packet hashes; run Architect review in an execution distinct from Author; audit exact final claims against locator-specific EvidenceUnits; validate CitationProjection against the audited fact draft; and bind publication to the projected draft hash. Artifacts synthesized after publication cannot retroactively satisfy an earlier gate.
20. Deterministic validation may enforce state order, hashes, ownership, capacity, coverage, and evidence specificity. It may not certify prose depth, continuity, claim support, or semantic review by counting titles, words, paragraphs, citation markers, or passed fields.

## Stable Identities and Visible Labels

Use stable IDs internally for recovery and cross-system lineage. Visible content uses natural human labels only.

| Entity | Internal identity pattern |
|---|---|
| Project | `prj_<uuidv7>` |
| Goal | `gol_<uuidv7>` plus version |
| Knowledge base | `kb_<uuidv7>` |
| Source | `src_<uuidv7>` plus Zotero item key |
| Container | `ctr_<uuidv7>` |
| Knowledge node | `kn_<uuidv7>` |
| Claim | `clm_<uuidv7>` |
| Evidence unit | `evu_<uuidv7>` |
| Relation | `rel_<uuidv7>` |
| Task | `tsk_<uuidv7>` |
| Operation | `op_<uuidv7>` |

Never place these identifiers in a Notion title, Notion prose heading, or ordinary Obsidian note title.

## Internal Handoffs

Skills may exchange structured handoff envelopes under `.knowledge-product/artifacts/`. Validate them with [validate_handoff.py](../scripts/validate_handoff.py). They are never review documents.

Required envelope semantics:

- identify the project, run, producer, stage, and checkpoint;
- reference immutable artifact revisions and checksums;
- identify unresolved decisions and risky proposed mutations;
- recommend, but do not directly invoke, the next owning Skill;
- return `needs_replan` when inputs or bindings drift.

Allowed handoff statuses are `ready`, `needs_question`, `needs_approval`, `needs_replan`, `needs_split`, `blocked`, `paused`, and `completed`. `needs_split` is an internal scheduling result: it asks the orchestrator to create smaller bounded work without dropping obligations or asking the user to continue. Domain states such as `optional_declined`, `no_candidate`, or `quarantined` belong inside the owned artifact.

## Mutation Authorization

The confirmed project brief establishes scoped authorization for ordinary, reversible writes inside newly created GDKP-managed targets, including:

- registering an approved source batch in the bound Zotero project collection;
- creating or revising workflow-owned Notion publication pages;
- creating or refreshing managed files in the project Obsidian Vault;
- writing machine state and requested outputs inside the project root.

For those writes, the system plans, applies idempotently, records the connector or filesystem result, and does not ask for a separate technical preview. It does not launch a content read-back audit after a successful Notion or Obsidian write.

Ask before a write only when it would delete data, overwrite user-authored content, affect an unapproved object or scope, incur material cost, expose credentials or sensitive data, resolve an ambiguous identity, or otherwise create significant risk. Approval binds the exact scope and expires when the material facts change.

## Completion and Recovery

- A successful Notion or Obsidian write result with the expected target identity is sufficient publication or projection evidence; do not spend another model pass rereading content for routine acceptance.
- Resolve the bound target before writing. An Obsidian connector open on another Vault is unavailable for the project and must not be used.
- Preserve user-authored content and recover from the last completed checkpoint.
- Treat runtime compaction as a replaceable conversation cache, never as canonical publication state. The external DraftPacket checkpoint in Project Kernel state or a referenced versioned artifact is the recovery authority.
- Bind each DraftPacket checkpoint to the current requirement, `FullBookChapterKnowledgeMap`, evidence, and publication revisions; preserve its knowledge obligations, queue position, accepted draft content or stable publication destination, continuity context, single-pass DraftQualityReview state, Zotero claim-audit state, CitationProjection state, and publish-operation state.
- Persist `LargePublicationRunState` and run [validate_large_publication_state.py](../scripts/validate_large_publication_state.py) before each forward transition. Append its state-bound hash-chained gate receipt to the run state and Kernel events; a final validator run or reconstructed receipt does not replace missing earlier gates.
- After compaction, restart, or agent transfer, reload the canonical map, Packet queue, accepted prose, and next work item from that checkpoint. A summary may not advance `pending` or `drafting` work to an accepted state or regenerate accepted prose from memory.
- A requirement, map, evidence, or draft revision mismatch invalidates the affected DraftQualityReview, Zotero claim audit, and pending publish state. Recover from the last matching checkpoint. A newly authored revision may receive its one pre-publication review; a repair prompted by that review does not. Do not add a Notion or Obsidian audit loop.
- Inspect an existing operation ID before retrying a possibly applied write.
- Missing connectors block only dependent work.
- Report the smallest useful status summary: what is finished, what remains, and any decision genuinely required.
- Do not create routine `approval-*`, `handoff-*`, `*-preview.*`, or `*-request.*` files for the user.

For a large publication, no chapter, first batch, title count, or completed exercise can satisfy the full-book completion barrier by itself. `knowledge-product-orchestrator` may report publication complete only after the `complete` gate passes: the canonical full-book map was frozen before authoring, every included obligation is assigned to an accepted checkpointed DraftPacket, the queue has no pending or stale work, each coherent unit has exactly one independent pre-publication DraftQualityReview with every finding resolved once, all final fact-bearing wording has a current locator-specific Zotero claim audit, every audited unit has a passing CitationProjection bound to that fact draft, and every required publication unit has a successful write result bound to the projected reader-facing hash. No second Architect review, post-write Notion semantic/reload audit, or Obsidian graph audit is part of this barrier. Only then may the default flow hand its main path to learner exercises or mastery validation.

Bundle maintainers run [validate_bundle.py](../scripts/validate_bundle.py) after changing a Skill, shared contract, UI metadata file, or helper.
