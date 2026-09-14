# Getting Started

[Documentation](README.md) | [Project README](../README.md)

## Requirements

- A current Codex environment with [Agent Skills support](https://developers.openai.com/codex/skills).
- Python 3.10 or later for the bundled validation and packaging helpers.
- [PyYAML](https://pyyaml.org/) for bundle and handoff validation.
- Access to Zotero, Notion, and Obsidian when the selected workflow uses those surfaces.

GDKP does not install or authenticate external application connectors. Full publication and graph verification require Codex to have readable and writable access to the intended external targets.

## How Codex Discovers GDKP

Codex scans `.agents/skills/` from the current working directory up to the repository root. GDKP therefore installs the complete bundle under the target project's `.agents/` directory.

The 13 skills share contracts and deterministic helpers. Install the bundle as a unit rather than copying an individual skill folder.

## Install

Clone this repository:

```bash
git clone https://github.com/Lovett-Ryan/GDKP.git gdkp
```

For a target project that does not already contain `.agents/`, run:

```bash
python3 gdkp/.agents/scripts/package_core_bundle.py \
  /path/to/your-project/.agents \
  --source-id GDKP-v1.0.0
```

The packager:

1. copies all core skills, shared references, and helper scripts;
2. verifies the staged file inventory;
3. writes a SHA-256 release manifest;
4. installs the snapshot atomically.

It deliberately refuses to merge into or overwrite an existing destination. If the target already has `.agents/`, stage GDKP in a separate directory and review naming and resource collisions before performing an explicit migration.

For a quick evaluation, open the cloned GDKP repository itself in Codex. Codex will discover the skills directly from `.agents/skills/`.

## Start a Project

Open the target project in Codex and explicitly invoke the control plane:

```text
Use $knowledge-product-orchestrator to start a GDKP project.

My goal is to build an evidence-backed, beginner-friendly textbook on
[topic]. I want broad field coverage, but mastery only for [focus areas].
Use [chosen sources], and ask before adding supplemental sources.
```

For a product goal:

```text
Use $knowledge-product-orchestrator to build [deliverable].
The result must satisfy [acceptance conditions].
Use [required inputs or standards] and keep [decisions] under my control.
```

Codex can also select a skill implicitly when a request clearly matches its description, but explicit invocation is the clearest entry point for an end-to-end project.

## Resume a Project

GDKP stores recoverable machine state under `.knowledge-product/`. To continue:

```text
Use $knowledge-product-orchestrator to resume this GDKP project from its
latest verified checkpoint.
```

The orchestrator validates the project context and routes work from the last verified state rather than restarting completed stages.

## Default Project Paths

```text
<project-root>/
├── .agents/              # Installed GDKP bundle
├── .knowledge-product/   # Local machine state
├── Obsidian/             # Project-local Vault
└── outputs/              # Requested deliverables
```

See [Architecture](architecture.md) for the role of each path and external application.
