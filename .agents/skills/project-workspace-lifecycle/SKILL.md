---
name: project-workspace-lifecycle
description: Initialize, attach, inspect, resume, relink, migrate, or detach a GDKP project, including its Project Kernel, root-level Zotero collection, Notion publication binding, project-local Obsidian Vault, and Skill registry. Use for workspace lifecycle and connector capability work; do not discover evidence, reconstruct requirements, author knowledge, or execute outcomes.
---

# Project Workspace Lifecycle

Create and maintain the recoverable boundary for one GDKP project.

## Required Contracts

Read [workflow-contracts.md](../../references/workflow-contracts.md) before returning a handoff or writing state. Read the relevant operation in [project-kernel.md](../../references/project-kernel.md). Read [managed-content-boundaries.md](../../references/managed-content-boundaries.md) before binding or adopting external content.

## Defaults

- Project state: `<project-root>/.knowledge-product/`
- Core and project Skills: `<project-root>/.agents/`
- Deliverables: `<project-root>/outputs/`
- Obsidian Vault: `<project-root>/Obsidian/`
- Zotero collection: one root-level `GDKP-<Project Name>` collection in the selected library
- Notion: one natural project publication root under a user-approved parent

Do not create Zotero subcollections or Notion Operations, Projects, Tasks, Decisions, Reviews, Questions, or Audit pages.

Normalize and record the exact Obsidian Vault path and its workflow-managed scope. When an Obsidian connector is available, read its active Vault information before binding or using it. The connector is usable for this project only when its normalized path resolves to the bound Vault. A mismatch is a degraded capability state; never read or write the unrelated active Vault.

## Operations

Choose one operation:

- `init`: find any existing Kernel, stage the local layout atomically, provision or bind the defaults within confirmed scope, record returned native identities, and checkpoint;
- `attach`: inventory existing objects, bind by stable identity, and preserve all user content;
- `doctor`: perform read-only integrity and capability checks and report a concise diagnosis;
- `resume`: continue from the latest verified checkpoint after inspecting pending operation IDs;
- `relink`: update moved paths or external bindings by stable and native identity;
- `migrate`: snapshot, transform, verify, and preserve recovery;
- `detach`: stop automation bindings and preserve lineage without deleting external content.

## Interaction Rules

Ordinary reversible creation of the default local folders, root-level project collection, workflow-owned Notion root, and hidden binding records does not require separate technical previews after the project brief is confirmed. Ask only for:

- a missing project root or external parent that cannot be inferred safely;
- an ambiguous object collision;
- adoption or overwrite of existing content;
- a destructive, costly, credential-sensitive, or out-of-scope operation.

Ask in Codex using natural language. Never ask the user to inspect binding YAML, a lifecycle receipt, or a mutation preview file.

## Invariants

- Stable IDs and external native IDs establish identity; titles and absolute paths do not.
- Preserve credentials outside the project.
- Keep machine artifacts internal and do not create routine user-review reports.
- Validate lifecycle bindings, native identities, paths, and returned operation results. Do not reread Notion publication content or Obsidian notes and graph settings as a publication audit.
- Distinguish scoped filesystem write results from connector-backed write results. Neither requires a second content or graph audit after success.
- Preserve user-authored Notion blocks and Obsidian notes.
- Modify `.obsidian/graph.json` only when the Vault or file is workflow-owned, or when the user explicitly authorizes adoption of that setting. Preserve unrelated application preferences.
- A project-local core snapshot is valid only when its Skill, reference, script, and manifest hashes agree.
- A third-party domain Skill is active only when its project lock, commit, audit, hash, scope, and host discovery agree.

## Output

For `doctor`, compare the stored Obsidian binding with both the resolved filesystem path and the connector-reported active Vault. Report a connector/path mismatch explicitly and keep connector-backed writes unavailable until it is corrected. This is target-safety diagnosis, not a graph-content audit.

Return ProjectContext, capability state, current bindings, Skill registry state, latest checkpoint, unresolved conflicts, and a recommended next owner to `knowledge-product-orchestrator`. These are machine artifacts. The user-facing result should state only what was attached or created and any action genuinely required.
