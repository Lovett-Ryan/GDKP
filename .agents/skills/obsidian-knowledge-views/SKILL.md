---
name: obsidian-knowledge-views
description: Build and refresh readable concept notes and a sparse, traceable native Obsidian graph from verified Notion publications. Use after publication or graph feedback; do not mirror Notion, generate map artifacts by default, force connectivity, use abstract containers as nodes, or overwrite user notes.
---

# Obsidian Knowledge Graph

Turn the formal Notion textbook into selective study notes and a cautious project relationship graph.

## Required Contracts

Read [workflow-contracts.md](../../references/workflow-contracts.md) before handoff. Read [view-projection-policy.md](../../references/view-projection-policy.md) for node, edge, note, and refresh rules. Read [knowledge-node-relation-schema.md](../../references/knowledge-node-relation-schema.md) for semantic relations and [managed-content-boundaries.md](../../references/managed-content-boundaries.md) before writing files.

## Preconditions

Require current ProjectContext, a verified NotionPublicationPack, framework node and relation data, Notion revisions, and an Obsidian binding. The default Vault is `<project-root>/Obsidian/`. If it exists, attach and preserve it; otherwise create it as a standalone Vault within the confirmed project scope.

Resolve the exact bound Vault path before reading or writing. When an Obsidian MCP is available, compare its reported Vault path with the stored binding. A mismatch makes that connector unavailable for this project; never read from or write to the unrelated Vault. Filesystem work may continue inside the bound project path when authorized, but it remains `local_files_verified` until the intended Vault or application view is read back.

## Graph Curation

1. Read the relevant Notion chapters as the verified factual basis.
2. Select only concrete, important, reusable concepts that improve understanding or recall. A valuable standalone concept may remain isolated.
3. Exclude containers, disciplines, courses, source records, tasks, metadata, and trivial details.
4. Select only relations with an explicit conceptual reason such as prerequisite, causal, derivational, compositional, contrastive, constraining, evaluative, or applicative meaning.
5. Reject links based only on shared keywords, citations, tags, page proximity, or co-occurrence.
6. Remove reciprocal repetition, redundant shortcuts, and transitive clutter. Zero to four strong visible links per note is the normal range; a genuine hub may exceed it only when every edge remains indispensable.
7. Create an internal GraphPlan and validate it autonomously. Do not ask the user to approve a center score, ViewSpec, macro/local mode, edge list, or preview.
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

Use short sections and enough context that a note is readable without opening its neighbors. Paraphrase and reorganize; do not copy the full textbook. Use strict LaTeX delimiters: `$...$` inline and `$$...$$` for display math. Do not introduce facts unsupported by the verified Notion content. Keep IDs, hashes, revisions, evidence lineage, importance tiers, and generator metadata in the hidden `.gdkp/` sidecar rather than visible notes.

## Output and Refresh

Use Markdown notes and Wikilinks so Obsidian's native Global Graph is the complete overview and native Local Graph is the interactive reading surface. The normal visible layout contains concept-note folders only; graph plans, importance tiers, hashes, and lineage remain under `.gdkp/`.

Mark the projection stale whenever the verified Notion publication revision advances. Refresh from that exact revision, reassessing whether every node and edge still deserves inclusion and updating every visible Notion backlink. Preserve user-authored files and edited regions. If a managed-file conflict cannot be reconciled safely, leave the user's version intact and report the specific conflict in Codex.

Before returning `graph_updated`, re-read the managed notes and verify that all files exist, every Wikilink target resolves, the unique actual edge set matches the GraphPlan, Notion backlinks point to the current verified publication, LaTeX contains no legacy delimiters or code-wrapped formulas, and any managed native Graph configuration persisted. Record separate semantic-edge and visible-file counts; do not count Canvas artifacts as knowledge nodes.

Exclude marked external increments while their origin status remains pending or accepted. Do not silently promote them.

Return an internal KnowledgeGraphManifest with verified files, edges, Notion lineage, exclusions, and conflicts to `knowledge-product-orchestrator`. The actual Vault and native graph are the user review surface.
