# Managed Content Boundaries

This policy prevents one application from absorbing another application's role and protects user-authored content.

## Zotero Boundary

The workflow owns only the project collection membership and metadata fields it created or explicitly adopted. It may normalize and deduplicate approved items, but it must not reorganize unrelated library content. The default project collection is the root-level `GDKP-<Project Name>` collection with no automatic subcollections.

## Notion Boundary

Notion is a formal publication surface. Workflow-owned pages may contain:

- textbook or monograph chapters for knowledge projects;
- requested product manuals, specifications, or reports;
- natural prose, equations, examples, tables, callouts, toggles, diagrams, citations, and references;
- nested pages when they improve the reader's conceptual hierarchy.

Never publish the following to Notion:

- user questions or answers;
- goals, task queues, project status, checkpoints, or schedules unless the user explicitly requests a final project report;
- candidate manifests, source audits, claim audits, evidence packs, validation output, receipts, hashes, stable IDs, or revision metadata;
- handoff envelopes, mutation previews, approval records, debugging information, or connector logs;
- Source View images, screenshots, thumbnails, bookmarks, preview cards, iframes, or embedded source pages in References.

Notion titles and visible headings must be natural. Do not use prefixes such as `Stable ID`, `Base Capsule`, `Core Content`, `Verification`, `Relation ID`, `Combination ID`, or type codes. Keep machine lineage in Project Kernel state or hidden connector properties.

Protect all pre-existing user blocks. A managed page or block must be identifiable internally. If that identity is absent or ambiguous, do not overwrite it.

## Obsidian Boundary

Obsidian is a selective study-note and relationship-graph surface. Managed visible files default to concise concept notes under `Concepts/`, with Wikilinks, relationship explanations, and a link back to the relevant Notion publication. They must not copy an entire Notion chapter or reproduce the internal workflow schema.

The native Global Graph and Local Graph are the default views over one semantic graph. Do not create a `Maps/` system, Canvas files, Mermaid maps, screenshots, or duplicated local-view artifacts unless the user explicitly requests that artifact. Isolated notes and disconnected graph components are valid when no defensible semantic relation exists.

Store graph lineage and generated-file hashes under `<vault>/.gdkp/`. Preserve user-created notes and user-edited regions. Refresh only files that are clearly marked as workflow-managed internally; on conflict, create a proposed sibling or ask before overwrite.

The default Vault is `<project-root>/Obsidian/`. A shared Vault requires an explicit user choice and a narrower managed folder. Modify `.obsidian/graph.json` only when it is workflow-owned or its adoption is explicitly authorized; preserve unrelated preferences. Never treat a connector pointed at another Vault as access to the bound project Vault.

## Local Project Boundary

The local project owns machine state, project-specific Skills, executable artifacts, experiments, and deliverables. Internal structure may be complex because Codex consumes it; user-facing summaries must remain simple. Do not treat `.knowledge-product/artifacts/` as a documentation product.

## Cross-System Rule

Each fact has one canonical role:

- Zotero proves where evidence came from;
- Notion explains the subject formally;
- Obsidian helps the learner see and remember selected relationships;
- the local project proves that work or a product was completed.

Synchronization means preserving lineage and updating the appropriate representation, not copying identical content into every system.
