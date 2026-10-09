# Project Kernel and Workspace Lifecycle

Use this contract for project identity, local layout, bindings, lifecycle operations, recovery, and capability health.

## Default Project Layout

```text
<project-root>/
|-- .agents/
|   |-- skills/
|   |-- references/
|   |-- scripts/
|   `-- core-bundle-manifest.yaml
|-- .knowledge-product/
|   |-- project.yaml
|   |-- bindings.local.yaml
|   |-- capabilities.json
|   |-- domain-skills.lock.yaml
|   |-- events.jsonl
|   |-- artifacts/
|   |-- snapshots/
|   `-- runtime.sqlite
|-- Obsidian/
`-- outputs/
```

`<project-root>/Obsidian/` is the default standalone Vault root. If it already exists, inspect and attach it without replacing user content. Use a shared or external Vault only when the user explicitly requests one.

The Kernel may store detailed structured state, but that structure is private to Codex. Do not populate the project with routine review reports or ask the user to inspect `.knowledge-product/`. Create a diagnostic report only when the user explicitly requests one or when it is needed to hand off a reproducible failure.

## Default External Bindings

### Zotero

Create or bind one root-level collection in the selected Zotero library:

```text
GDKP-<Project Name>
```

The collection is directly under the library root. Do not create automatic subcollections. Bind by the stored Zotero collection key and project identity; a matching title alone is not sufficient to merge or adopt an existing collection.

### Notion

Bind a publication root under a user-approved Notion location. A knowledge project publishes textbook or monograph content there. A product project publishes only a requested final manual, specification, or report. Do not provision Operations, Projects, Tasks, Decisions, Reviews, Questions, or Audit pages.

### Obsidian

Bind the Vault to `<project-root>/Obsidian/` by default. Store its normalized resolved path, native identity when available, and the exact workflow-managed scope. Store machine lineage under a hidden `.gdkp/` directory inside the Vault; keep visible notes natural and reader-oriented.

Before using an Obsidian connector or MCP, read its active Vault information and compare the normalized path with the binding. Only an exact bound-Vault match is an available connector-backed write capability. A mismatch may still permit carefully scoped filesystem preparation inside the intended project Vault, but it never permits reads or writes in the unrelated active Vault.

## Identity and State

Stable IDs identify projects and cross-system objects; titles and paths are mutable labels. Keep both the GDKP ID and the external native ID in `bindings.local.yaml` or the identity map. Never expose these IDs as ordinary publication headings.

State authority is split as follows:

- `events.jsonl`: append-only execution facts;
- revisioned artifacts: machine declarations and checksums;
- `runtime.sqlite`: rebuildable query index;
- external applications: canonical content only within their assigned role.

For a large publication, the Kernel also persists `LargePublicationRunState` as defined in [large-publication-state-contract.md](large-publication-state-contract.md), its hash-chained gate receipts, the canonical `FullBookChapterKnowledgeMap` reference, DraftPacket queue, packet checkpoints, accepted draft content or stable page destinations, single-pass DraftQualityReview state and finding dispositions, Zotero claim-audit state, publication-operation state, continuity capsules, and the next schedulable packet. Each successful prospective gate receipt is appended to both the run state and `events.jsonl` before the next owner is dispatched. Runtime compaction is a replaceable working cache, not state authority. After compaction, restart, or agent handoff, reload these records rather than reconstructing accepted prose from model memory.

Credentials never belong in the project directory.

## ProjectContext

A valid ProjectContext identifies the project, resolved root, lifecycle and binding revisions, capability state, active project Skills, and latest verified checkpoint. It may be serialized internally. Consumers validate its checksum and revision before writing.

A project run lease scopes concurrent writes to one project. Cross-project evolution requires a separate target-project context and lease. A lease is an internal concurrency control, not a user approval document.

## Lifecycle Operations

### Initialize

1. Resolve the requested root and search upward for an existing Kernel.
2. Inspect the target and connector capabilities without mutation.
3. Confirm the brief if the goal or external scope is not already clear.
4. Stage and atomically create the local Kernel, `outputs/`, and default `Obsidian/` Vault.
5. Create or bind the root-level Zotero collection and Notion publication root within the confirmed project scope.
6. When an Obsidian connector is available, confirm that it reports the intended Vault before connector-backed setup or writing. Configure workflow-owned graph settings only in the actual Vault; do not create a duplicate `.obsidian/` at the project root when the Vault is its `Obsidian/` child.
7. Record returned native identities, stable bindings, capability levels, and the checkpoint. Do not reread publication or graph content merely to audit the write.

Do not ask for separate technical previews for these ordinary, reversible, workflow-owned writes. Stop for an ambiguous collision, an existing object that would need adoption, a permission problem, cost, or any user-content change.

### Attach

Inspect existing local and external objects. Bind by stable identity when possible. Ask only when the user must choose between ambiguous objects or authorize adoption of existing content. Reference mode never changes content; adopt mode may add only agreed managed metadata; provision mode creates new workflow-owned objects.

### Doctor

Perform read-only checks of layout, hashes, bindings, connectors, leases, pending operations, and Skill integrity. Compare the bound Obsidian path with both the resolved filesystem location and connector-reported active Vault. Report a concise diagnosis. Do not repair unless the user asks for repair or the original request already includes it.

### Resume

Continue from the latest durable checkpoint. Before retrying a prepared or possibly applied operation, query the target by operation ID or stable identity. Preserve completed work.

For a DraftPacket, validate the bound map, requirement, framework, evidence, body, and binding revisions, then rerun the appropriate gate in [validate_large_publication_state.py](../scripts/validate_large_publication_state.py). A summary cannot advance `queued`, `dispatched`, or `checkpointed` state to accepted. A hash or revision mismatch invalidates the affected DraftQualityReview, Zotero claim audit, CitationProjection, and publication state and resumes from the last durable checkpoint; context pressure causes a smaller packet or another internal pass, never a summary rewrite of accepted prose. Preserve whether the current publication run already consumed its single Architect review: an unchanged draft is not reviewed again, and a repair prompted by that review proceeds directly to claim audit. Do not recover by rereading Notion or Obsidian content.

### Relink

Resolve moved paths or changed external objects using stable and native IDs. Ask only for ambiguous identity or an out-of-scope target. Increment the binding revision and preserve binding history.

### Migrate

Snapshot governed state, validate compatibility, apply a reversible migration, and verify it. Ask before destructive transformation, user-content overwrite, or loss of backward compatibility.

### Detach

Stop automation bindings and preserve a tombstone and lineage. Leave external content intact. Deletion is a separate explicit request.

## Mutation and Recovery

For every write, internally record a stable operation ID, expected target, managed scope, input revision, and returned result. Ordinary writes covered by the confirmed project scope proceed without another user gate. A successful connector response carrying the intended native identity is sufficient operational evidence; do not add publication-content or graph read-back audits. Compensation may touch only workflow-owned content.

An unavailable connector blocks only its dependent result:

| Condition | Still allowed | Do not claim |
|---|---|---|
| Zotero not writable | Source planning and local capture | Sources admitted or registered |
| Notion not writable | Local publication draft | Notion publication completed |
| Obsidian unavailable | Graph plan and queued files | Vault refreshed |
| Obsidian connector on another Vault | Scoped files in the intended Vault, labeled `local_files_verified` | Connector-backed Vault or graph write completed |
| GitHub unavailable | Verified pinned project Skills | Discovery, install, or update |
| Skill integrity drift | Quarantine and fallback | Active capability |

## Core and Domain Skill Integrity

Install the complete core bundle with [package_core_bundle.py](../scripts/package_core_bundle.py); do not copy one core Skill without its matching references and helpers. Project-acquired third-party Skills remain in `<project-root>/.agents/skills/`, are pinned by immutable commit and tree hash, and are governed by `domain-skills.lock.yaml`. Integrity drift causes quarantine, never a silent download or update.
