---
name: domain-skill-acquisition
description: Evaluate a verified domain capability gap, discover and compare eligible GitHub Skills, own the explicit Q5 authorization, audit and install the exact approved Skill at project scope, and preserve immutable provenance. Use only when a specialized capability affects an outcome; do not perform the downstream domain task or treat a downloaded Skill as evidence or a control plane.
---

# Domain Skill Acquisition

Add a specialized project capability without weakening GDKP ownership, safety, or provenance.

## Required Contracts

Read [workflow-contracts.md](../../references/workflow-contracts.md) before handoff. Read [domain-capability-gap-policy.md](../../references/domain-capability-gap-policy.md) before accepting a trigger. Read [question-gates.md](../../references/question-gates.md) before Q5. Read the relevant discovery, audit, naming, and lifecycle sections of [github-skill-acquisition-policy.md](../../references/github-skill-acquisition-policy.md).

## Trigger

Act only on a verified DomainCapabilityGap or an explicit request for a specific GitHub Skill that can be normalized into one. First reuse an active compatible project Skill when available. An unfamiliar field or desire for a stronger method is not enough.

## Discovery and Q5

1. Inspect GitHub read-only and resolve candidates to immutable commits.
2. Evaluate at most three eligible candidates for capability fit, maintenance, license, transparency, dependency burden, permission exposure, conflicts, and testability.
3. Present Q5 as a concise Codex comparison, not a manifest dump.
4. Disclose repository path, commit, license, purpose, limitations, scripts, dependencies, network and filesystem behavior, permissions, project destination, visible name, and fallback.
5. Bind approval to the exact candidate, commit, content hash, project scope, destination, and permissions. Silence is not approval.

On refusal or no eligible candidate, use the safe generic fallback and state its concrete limitation. Block only when a mandatory acceptance condition cannot be met safely.

## Installation

After approval:

1. stage only the approved repository path and commit outside the active Skill directory;
2. audit every instruction, metadata file, script, asset, dependency, hook, symlink, executable, and permission request;
3. stop for a material mismatch and request a new Q5;
4. adapt only approved interface naming or path references;
5. use canonical name `<project-slug>-<field-slug>-<upstream-skill-slug>`;
6. set the Codex display name to `[Project Name]-[Field] <Upstream Skill Name>`;
7. preserve upstream identity, commit, license, hashes, permissions, and adaptation diff in the project lock;
8. validate safely, install atomically under `<project-root>/.agents/skills/`, and verify host discovery.

Do not broaden implicit invocation. If discovery requires restart, return `activation_pending`, not active. Quarantine drift and never follow a moving branch silently.

## Downstream Boundary

Return the active capability handle to `knowledge-product-orchestrator`, which resumes the owning core Skill. The acquired Skill may not approve sources, publish canonical Notion content, manage the Obsidian graph, change Goal or Task ownership, request broader authority for itself, or route the workflow.

Keep candidate manifests, audit details, locks, and receipts internal unless the user explicitly asks for a security audit. Q5 itself remains a short natural-language decision in Codex.
