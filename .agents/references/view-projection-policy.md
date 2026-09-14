# Obsidian Knowledge Graph Policy

GDKP V1.0 creates one curated project knowledge graph: one semantic graph presented through Obsidian's native Global Graph and Local Graph. It does not generate separate macro/local graph ontologies or map files by default.

## Purpose

Obsidian should resemble high-quality student notes built from a formal Notion textbook. It selects, paraphrases, and reconnects the knowledge most useful for understanding and recall. It is neither a Notion mirror nor a second canonical publication.

## Default Vault

Use `<project-root>/Obsidian/`. Create it as a standalone Vault during project initialization when absent. Attach it when present and preserve user content. Use an external or shared Vault only by explicit request.

Suggested managed layout:

```text
Obsidian/
|-- Concepts/
`-- .gdkp/
    |-- graph-manifest.json
    `-- lineage.jsonl
```

Visible folder names may adapt to the subject. `.gdkp/` is hidden machine state.

The stored binding, filesystem target, and any connected Obsidian MCP must resolve to the same Vault before connector-backed verification. If an MCP reports another Vault, treat it as unavailable for this project and do not touch that Vault.

## Node Selection

Include a concept only when all of the following are true:

1. it is concrete and independently meaningful;
2. it is important to the project's learning or product reasoning;
3. it is reusable beyond one sentence or isolated fact;
4. its note can be supported by verified Notion publication content.

A concept may remain isolated or belong to a disconnected component. Connectivity is an outcome of justified relations, not an admission requirement.

Exclude fields, disciplines, courses, chapters used only as containers, source records, authors, tasks, project state, metadata, trivial implementation details, and narrow facts that do not improve the graph.

Prefer omission over a noisy node. Record a small editorial importance tier such as core, supporting, or contextual for presentation, without exposing machine scores in the note.

## Edge Selection

Every link must have a readable reason. Suitable relations include prerequisite, enables, causes, derives, composes, contrasts, specializes, implements, constrains, evaluates, and applies-to.

Do not create an edge merely because two notes:

- share a source, keyword, tag, or parent chapter;
- appear next to each other in Notion;
- co-occur in generated text;
- are transitively connected through a clearer intermediate concept.

Keep the graph sparse. Zero to four high-value links is the normal editorial range; a genuine hub may exceed it only when each additional link is indispensable. Remove reciprocal repetition, redundant shortcuts, and weak edges during refresh. Do not connect components merely to make the graph look complete.

## Student-Note Content

A concept note normally contains:

1. a one-sentence personal-understanding summary;
2. the key idea, mechanism, formula, or rule;
3. a small set of important Wikilinks with one or two sentences explaining each relationship;
4. an optional misconception, application, or memory cue;
5. a natural link to the relevant Notion chapter.

Do not copy the full chapter. Do not expose stable IDs, audits, projection hashes, or origin records in visible prose. The note may reorganize and paraphrase Notion content but may not introduce unsupported factual claims.

## Native Graph Output

Use ordinary Markdown notes and Wikilinks so Obsidian's native graph is the visualization. The visible managed output should not contain a `Maps/` folder, Canvas, Mermaid, graph screenshots, or duplicate local projections unless the user explicitly requests that exact artifact.

Use Global Graph for the complete overview. Use the native Local Graph, depth slider, hover, filters, and linked tabs for interactive locality. Several Graph tabs may coexist, but they remain views over one semantic graph rather than separate graph files.

When the active Vault configuration is workflow-owned:

- restrict the default graph to the managed concept path;
- hide attachments and unresolved links;
- keep orphan nodes visible;
- use a small number of native color groups to show editorial importance;
- allow native link degree to determine relative node size;
- use thinner links and moderate repulsion when density harms label readability.

Native Graph does not support arbitrary per-node sizing by importance. Never fabricate relations to manipulate size; exact manual sizing requires a separately authorized plugin or custom styling.

The internal GraphPlan records selected concepts, supported relationships, Notion revision lineage, exclusions, and conflict handling. It is generated and validated by AI; it is not a user approval document. The KnowledgeGraphManifest records the verified files and edges after write-back.

## Refresh Rules

- Refresh after relevant Notion publication changes.
- Treat every newer verified Notion publication revision as invalidating the prior Obsidian projection until refresh and read-back succeed.
- Re-evaluate whether each node and edge still earns inclusion; do not only append.
- Preserve user-authored notes and user-edited regions.
- Keep accepted external increments out of ordinary graph notes when their `origin_status` remains `external_pending` or `external_accepted`, unless the user explicitly promotes them later.
- On managed-file conflict, do not overwrite silently. Preserve the current file and report the specific conflict in Codex.

Verification requires the actual unique Wikilink edge set to match the GraphPlan, every target and current Notion backlink to resolve, and any managed Graph settings to be read back. Filesystem-only validation is not application verification when the bound app or MCP points at another Vault.

The actual Vault and native graph are the user review surface. Feedback produces a new graph revision without a separate schema or preview approval.
