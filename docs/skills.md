# Core Skills

[Documentation](README.md) | [Project README](../README.md)

GDKP 1.1.0 contains 14 coordinated Codex skills. They are released and versioned together as one bundle.

| Skill | Responsibility |
|---|---|
| [`knowledge-product-orchestrator`](../.agents/skills/knowledge-product-orchestrator/SKILL.md) | Starts, resumes, routes, and completes the end-to-end workflow |
| [`project-workspace-lifecycle`](../.agents/skills/project-workspace-lifecycle/SKILL.md) | Initializes, attaches, inspects, migrates, and recovers project workspaces and application bindings |
| [`intent-source-analysis`](../.agents/skills/intent-source-analysis/SKILL.md) | Confirms the outcome, breadth, depth, source boundary, and retained user decisions |
| [`requirement-reconstruction`](../.agents/skills/requirement-reconstruction/SKILL.md) | Produces traceable requirements, the goal contract, optional coverage contract, and work-package graph |
| [`knowledge-framework`](../.agents/skills/knowledge-framework/SKILL.md) | Designs publication hierarchy, knowledge nodes, claim intents, semantic relations, and coverage audits |
| [`large-publication-architect`](../.agents/skills/large-publication-architect/SKILL.md) | Produces complete full-book maps and DraftPacket boundaries, then reviews each coherent large-publication draft once before publication |
| [`zotero-source-gate`](../.agents/skills/zotero-source-gate/SKILL.md) | Builds structural baselines, registers and admits evidence, and audits exact factual claims |
| [`notion-node-author`](../.agents/skills/notion-node-author/SKILL.md) | Writes and repairs large units once from the pre-publication review, then publishes source-audited reader-facing content without post-write audits |
| [`notion-natural-prose-editor`](../.agents/skills/notion-natural-prose-editor/SKILL.md) | Optionally refines bounded drafts after an explicit request or concrete prose feedback |
| [`obsidian-knowledge-views`](../.agents/skills/obsidian-knowledge-views/SKILL.md) | Writes selective concept notes and a sparse native graph once from source-audited publications |
| [`outcome-orchestrator`](../.agents/skills/outcome-orchestrator/SKILL.md) | Executes learning or product work and verifies acceptance evidence |
| [`knowledge-base-reuse`](../.agents/skills/knowledge-base-reuse/SKILL.md) | Establishes optional, traceable reuse of a qualified existing GDKP knowledge base |
| [`knowledge-base-evolution`](../.agents/skills/knowledge-base-evolution/SKILL.md) | Coordinates optional evidence-backed updates into an existing knowledge base |
| [`domain-skill-acquisition`](../.agents/skills/domain-skill-acquisition/SKILL.md) | Audits and installs an approved project-scoped GitHub skill when a verified capability gap exists |

## Ownership Model

- The orchestrator routes work but does not author another skill's artifacts.
- Each artifact type has one core owner.
- Stale or invalid inputs return to their owner for revision.
- Writes to the same target are serialized; independent non-conflicting work may run in parallel.
- A third-party project skill can extend domain capability but cannot replace the GDKP control plane.

Every core skill contains a required `SKILL.md` and an `agents/openai.yaml` file with Codex-facing metadata. Skill-specific resources stay inside the skill; shared contracts live in [`.agents/references/`](../.agents/references/).
