# Governance

[Documentation](README.md) | [Project README](../README.md)

GDKP automates routine reversible work while reserving consequential choices for the user.

## Expected Decisions

An ordinary new knowledge project should need no more than two expected decision moments:

1. A compact intake confirming the outcome and source boundary.
2. One decision on any concrete supplemental-source shortlist proposed by Codex.

The first intake may also separate coverage breadth from learning depth. A request for broad awareness and selective mastery keeps the full field visible while changing how deeply each topic is taught.

## Conditional Gates

| Gate | Trigger | If declined |
|---|---|---|
| **Q3 — Reuse** | A qualified existing knowledge base could materially improve the current project | Build independently |
| **Q4 — Evolve** | New evidence has a supported and useful relationship to an existing knowledge base | Leave the existing knowledge base unchanged |
| **Q5 — Acquire a skill** | A verified capability gap affects the outcome and an eligible GitHub skill exists | Use the safe generic fallback or report the unmet condition |

GDKP reuses valid earlier decisions until the governing goal, source policy, candidate set, target, risk, or requested permissions materially change.

For a confirmed large publication, internal `DraftPacket` boundaries, checkpoint writes, runtime-compaction recovery, and automatic continuation are managed execution details rather than user decision gates. The complete chapter-to-knowledge map is visible for review, but becomes an approval gate only when the user explicitly reserves that decision.

## Safety Decisions

GDKP asks before an action would:

- delete or irreversibly alter data;
- overwrite user-authored content;
- write outside the approved project or external binding;
- create a material charge;
- use or expose a credential or sensitive dataset in a new way;
- choose between ambiguous external objects;
- materially expand the goal, audience, source boundary, or risk.

Routine reversible writes inside a confirmed GDKP-managed scope do not require repeated approval.

## Managed-Content Boundaries

- Credentials stay outside the project bundle and project state.
- Stable IDs and external native IDs establish identity; titles and paths do not.
- GDKP preserves user-authored Notion blocks and Obsidian notes.
- An Obsidian connector is used only when its active Vault resolves to the project-bound Vault.
- Notion completion requires a current Zotero claim audit and a successful write result tied to the intended native page; a coherent large-publication unit must also have completed its one pre-publication semantic review and finding disposition. Completion never requires content reload.
- A newly source-audited Notion revision makes its earlier Obsidian projection outdated until the current scoped write succeeds.
- A downloaded skill is executable guidance, not factual evidence.
- Runtime compaction is a replaceable conversation cache; accepted large-publication content and progress are restored only from persistent `DraftPacket` checkpoints and publication-operation state.
- PublicationCoverageIndex assigns obligations prospectively to completed Packets and intended pages. Each coherent large-publication draft receives at most one pre-publication semantic review and one repair opportunity; GDKP does not re-review the repair or add Notion semantic/reload audits or Obsidian graph/read-back audits after successful writes.
- Exercises and mastery checks do not block completion of the remaining publication unless the user explicitly selects an interactive gated-course mode.

Third-party domain skills require an explicit Q5 decision, an immutable upstream commit, license and permission review, a project-local lock, and post-install validation.

## Scope and Limitations

- GDKP does not install or authenticate external application connectors.
- Publication and graph writes require writable access to the intended targets; target identity must be resolvable before mutation.
- A source-audited publication is not proof of learning; learning goals require separate acceptance evidence.
- A completed task record is not proof that a product works; product goals require tests, inspection, or another declared verification method.
- The core packager does not merge with an existing `.agents/` directory.
- GDKP 1.1.0 is a repository-scoped skill bundle, not a standalone application.

The canonical machine-facing policies are in [`.agents/references/`](../.agents/references/), especially `question-gates.md`, `managed-content-boundaries.md`, and `workflow-contracts.md`.
