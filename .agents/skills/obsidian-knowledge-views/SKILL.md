---
name: obsidian-knowledge-views
description: Build and refresh readable concept notes and a sparse native Obsidian graph from source-audited published Notion content, using one direct write pass without post-write graph or note audits. Use after publication or graph feedback; do not mirror Notion, force connectivity, use abstract containers as nodes, generate map artifacts by default, or overwrite user notes.
---

# Obsidian Knowledge Graph

Turn the formal Notion textbook into selective study notes and a cautious project relationship graph.

## Required Contracts

Read [workflow-contracts.md](../../references/workflow-contracts.md) before handoff. Read [view-projection-policy.md](../../references/view-projection-policy.md) for node, edge, note, and refresh rules. Read [knowledge-node-relation-schema.md](../../references/knowledge-node-relation-schema.md) for semantic relations and [managed-content-boundaries.md](../../references/managed-content-boundaries.md) before writing files.

## Preconditions

Require current ProjectContext, a NotionPublicationPack produced from Zotero-audited prose, framework node and relation data, the published Notion revision, and an Obsidian binding. The default Vault is `<project-root>/Obsidian/`. If it exists, attach and preserve it; otherwise create it as a standalone Vault within the confirmed project scope.

Resolve the exact bound Vault path before writing. When an Obsidian MCP is available, compare its reported Vault path with the stored binding. A mismatch makes that connector unavailable for this project; never read from or write to the unrelated Vault. This one path check is a safety boundary, not a graph audit. Filesystem work may continue inside the bound project path when authorized.

## Graph Curation

1. Use the relevant published Notion chapters as the source-audited factual basis.
2. Select only concrete, important, reusable concepts that improve understanding or recall. A valuable standalone concept may remain isolated.
3. Exclude containers, disciplines, courses, source records, tasks, metadata, and trivial details.
4. Select only relations with an explicit conceptual reason such as prerequisite, causal, derivational, compositional, contrastive, constraining, evaluative, or applicative meaning.
5. Reject links based only on shared keywords, citations, tags, page proximity, or co-occurrence.
6. Remove reciprocal repetition, redundant shortcuts, and transitive clutter. Zero to four strong visible links per note is the normal range; a genuine hub may exceed it only when every edge remains indispensable.
7. Create one internal GraphPlan and write from it directly. Do not run a second model pass to audit the plan, and do not ask the user to approve a center score, ViewSpec, macro/local mode, edge list, or preview.
8. Do not require the graph to be globally connected. Separate components and orphan nodes are valid when the subject structure supports them.

## Native Graph Presentation

- Publish one complete semantic graph through Markdown and Wikilinks. Do not create a `Maps/` folder, Canvas, Mermaid, screenshots, or generated graph documents unless the user explicitly requests that exact artifact.
- Treat Global Graph and Local Graph as interactive views over the same relationship set. Locality is provided by Obsidian's native Local Graph, depth control, hover, filters, tabs, and linked views—not by generated duplicate maps.
- Assign concepts to a small number of editorial importance tiers in the internal GraphPlan. Express tiers with native color groups or filters only when the active Vault configuration is workflow-owned.
- Let Obsidian derive relative node size from real link degree. Never add weak links to enlarge a node, and never claim that native Graph can assign arbitrary per-node sizes.
- Hide attachments and unresolved targets by default. Keep orphan display enabled so isolated but useful concepts remain visible.
- Restrict the default Global Graph to the managed concept folder when the surrounding Vault contains non-knowledge files. Preserve unrelated existing graph settings.

## Student Notes

Each managed note should normally provide:

- one sentence capturing the concept in learner-friendly language;
- its key mechanism, formula, rule, or intuition;
- a small set of Wikilinks with one or two sentences explaining each relationship; place each graph edge in one natural note rather than repeating navigation links mechanically;
- an optional misconception, application, or memory cue;
- a natural link to the relevant Notion chapter.

Use short sections and enough context that a note is readable without opening its neighbors. Paraphrase and reorganize; do not copy the full textbook. Use strict LaTeX delimiters: `$...$` inline and `$$...$$` for display math. Do not introduce facts unsupported by the source-audited Notion content. Keep IDs, hashes, revisions, evidence lineage, importance tiers, and generator metadata in the hidden `.gdkp/` sidecar rather than visible notes.

## Output and Refresh

Use Markdown notes and Wikilinks so Obsidian's native Global Graph is the complete overview and native Local Graph is the interactive reading surface. The normal visible layout contains concept-note folders only; graph plans, importance tiers, hashes, and lineage remain under `.gdkp/`.

Mark the projection outdated whenever the published Notion revision advances. Refresh from that revision in one pass, reassessing node and edge selection while generating the replacement and updating visible Notion backlinks. Preserve user-authored files and edited regions. If a managed-file conflict cannot be reconciled safely, leave the user's version intact and report the specific conflict in Codex.

After a successful file or connector write, return `graph_updated` without rereading notes, recounting nodes or edges, resolving every Wikilink, comparing the written graph with GraphPlan, or auditing native Graph settings. A reported write error or managed-file conflict remains actionable, but it does not authorize a broad read-back audit.

Exclude marked external increments while their origin status remains pending or accepted. Do not silently promote them.

Return a compact KnowledgeGraphManifest containing intended written files, planned edges, Notion lineage, operation results, exclusions, and conflicts to `knowledge-product-orchestrator`. Do not create verification receipts. The actual Vault and native graph are the user review surface, and later user feedback starts a targeted revision.
