# Workflow Contracts

This is the canonical coordination contract for GDKP V1.0. It separates durable machine state from the material a person is expected to read.

## Product Model

Codex is the control plane. It interprets the goal, schedules the owning Skills, keeps resumable state, and reports only decisions or results that matter to the user.

| Surface | V1.0 role | Must not become |
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

User-specified sources are acknowledged during intake and are pre-authorized for project registration. After those decisions, Codex autonomously reconstructs requirements, designs the framework, admits evidence, writes a complete Notion draft, applies the natural-prose pass, audits its final fact-bearing wording, publishes and reload-verifies it, then refreshes the Obsidian projection from that verified revision. The published Notion pages and actual Obsidian Vault are the review surfaces. Feedback on either surface starts a revision; it does not require a separate pre-publication document.

Textbooks, curricula, comprehensive surveys, field-level learning maps, and other unusually broad knowledge goals use the coverage-first branch defined in [curriculum-coverage-policy.md](curriculum-coverage-policy.md). In that branch, breadth and per-topic depth are confirmed separately, structural sources establish a CoverageBaseline before final framework design, and a passing coverage audit is required before the framework may be described as complete. Structural discovery may precede framework confirmation; it is not publication authoring or factual claim admission. When Zotero is unavailable, a hashed and read-back user-authorized local structural document may yield `coverage_local_verified` for framework work, but it cannot be promoted to factual evidence or final publication readiness without normal admission.

```text
setup
-> brief_confirmed
-> sources_confirmed
-> composing
-> publication_verified
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
-> composing in verified publication units
-> publication_verified
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
| CandidateManifest, CoverageBaseline, EvidencePack, SourceAuditReport, ClaimAuditReceipt | `zotero-source-gate` | Requirements, framework, Notion, outcomes |
| NaturalProseRevisionMemo | `notion-natural-prose-editor` | Notion Author |
| DraftClaimSet, PublicationCoverageIndex, and NotionPublicationPack | `notion-node-author` | Zotero, Obsidian |
| GraphPlan and KnowledgeGraphManifest | `obsidian-knowledge-views` | Outcomes, evolution |
| ReuseLineage and Q3 | `knowledge-base-reuse` | Requirements, framework |
| EvolutionChangeSet and Q4 | `knowledge-base-evolution` | Core owners through Codex |
| TaskSpec, TaskGraph, OutcomeEvidence | `outcome-orchestrator` | Codex and local executors |
| DomainSkillCandidateManifest, lock entry, receipt, and Q5 | `domain-skill-acquisition` | Lifecycle and Codex |

One Skill may request another owner's work but may not take ownership of it. Every core Skill returns control to `knowledge-product-orchestrator`.

## Evidence and Publication Invariants

1. Factual Notion publication content must be supported by admitted Zotero evidence and an internal claim audit.
2. Requirement coverage and domain coverage are different claims. A broad-domain framework is not coverage-verified without a current CoverageBaseline, one disposition for every baseline topic, governed omissions, prerequisite closure, and a passing coverage audit.
3. Learner adaptation changes sequence, scaffolding, notation load, examples, and depth. It never silently removes major topics from a requested broad field map.
4. Structural sources establish curriculum coverage only. A table of contents, syllabus, taxonomy, or survey outline does not by itself support the factual claims inside a publication.
5. Claim audits are quality controls, not user approval gates.
6. Notion uses natural titles and editorial prose. Stable IDs, revisions, evidence hashes, and audit receipts remain hidden in Project Kernel state or connector properties.
7. Notion equations use strict LaTeX in native equation objects. Publication is verified only after persistence and reload confirm section continuity, equation rendering with zero raw delimiters, citations, and References.
8. Notion references contain a formatted citation and a clickable original URL. They never contain Source View images, screenshots, thumbnails, bookmarks, iframes, or other previews.
9. Obsidian may paraphrase and reorganize only verified Notion content as study notes, and it must not introduce unsupported facts.
10. An Obsidian graph contains concrete, meaningful concepts and defensible semantic links. Containers, fields, courses, sources, tasks, and metadata are not graph nodes. It may contain isolated nodes or disconnected components; connectedness is never forced.
11. The default Obsidian output is one semantic graph rendered by native Global Graph and Local Graph views. Maps, Canvas files, screenshots, and manually duplicated local graphs are opt-in artifacts, not default output.
12. A new verified Notion revision immediately makes its earlier Obsidian projection stale until that exact publication revision is refreshed and read back from the bound Vault.
13. Product completion requires a verified deliverable and acceptance evidence. Knowledge completion requires evidence that the learner can use the knowledge, not merely that content was collected.
14. A GitHub-acquired Skill is an execution dependency, never factual evidence or a second control plane.

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

Allowed handoff statuses are `ready`, `needs_question`, `needs_approval`, `needs_replan`, `blocked`, `paused`, and `completed`. Domain states such as `optional_declined`, `no_candidate`, or `quarantined` belong inside the owned artifact.

## Mutation Authorization

The confirmed project brief establishes scoped authorization for ordinary, reversible writes inside newly created GDKP-managed targets, including:

- registering an approved source batch in the bound Zotero project collection;
- creating or revising workflow-owned Notion publication pages;
- creating or refreshing managed files in the project Obsidian Vault;
- writing machine state and requested outputs inside the project root.

For those writes, the system still plans, applies idempotently, reads back, verifies, and logs internally, but does not ask for a separate technical preview.

Ask before a write only when it would delete data, overwrite user-authored content, affect an unapproved object or scope, incur material cost, expose credentials or sensitive data, resolve an ambiguous identity, or otherwise create significant risk. Approval binds the exact scope and expires when the material facts change.

## Completion and Recovery

- A connector response is not completion until the target is read back and verified.
- A local file check is not application verification when the connector is open on a different Vault or the target application has not loaded the change.
- Preserve user-authored content and recover from the last verified checkpoint.
- Inspect an existing operation ID before retrying a possibly applied write.
- Missing connectors block only dependent work.
- Report the smallest useful status summary: what is finished, what remains, and any decision genuinely required.
- Do not create routine `approval-*`, `handoff-*`, `*-preview.*`, or `*-request.*` files for the user.

Bundle maintainers run [validate_bundle.py](../scripts/validate_bundle.py) after changing a Skill, shared contract, UI metadata file, or helper.
