# Development

[Documentation](README.md) | [Project README](../README.md)

## Repository Layout

`.agents/` is the canonical bundle. The public source repository should not contain a second top-level copy of its skills, shared references, or scripts.

```text
GDKP/
├── .agents/
│   ├── core-bundle-manifest.yaml
│   ├── references/               # Shared contracts, schemas, and policies
│   ├── scripts/                  # Deterministic validators and packager
│   └── skills/                   # The 14 core Codex skills
├── docs/                         # English documentation
│   └── *.md
├── LICENSE
└── README.md
```

## Validation

Install the only non-standard-library validation dependency:

```bash
python3 -m pip install PyYAML
```

Validate the canonical bundle:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 .agents/scripts/validate_bundle.py .agents
```

Validate individual workflow artifacts when needed:

```bash
python3 .agents/scripts/validate_handoff.py path/to/handoff.yaml

python3 .agents/scripts/validate_claim_audit.py \
  path/to/draft-claim-set.json \
  --receipt path/to/claim-audit-receipt.json

python3 .agents/scripts/validate_citation_projection.py \
  path/to/projected-draft.md \
  --source-draft path/to/audited-fact-draft.md \
  --manifest path/to/citation-projection.json \
  --draft-claims path/to/draft-claim-set.json \
  --evidence-pack path/to/evidence-pack.json

python3 .agents/scripts/validate_coverage_audit.py \
  path/to/coverage-audit.json
```

The bundle validator checks the core inventory, skill metadata, shared references, relative links, English-only skill content, UI metadata, and release manifest.

## Version and Integrity

The current bundle version is **1.1.0**.

All 14 core skills are released together under this bundle version. Repository `SKILL.md` files do not declare independent semantic versions: the supported identity metadata is `name` and `description`, while release identity and integrity are recorded at bundle level.

`.agents/core-bundle-manifest.yaml` records:

- bundle and schema versions;
- a synchronized version entry for each of the 14 core skills;
- release source identity;
- a SHA-256 digest for every core skill, shared reference, and helper script;
- a deterministic digest of the complete core tree.

Create a fresh, non-merging project snapshot with:

```bash
python3 .agents/scripts/package_core_bundle.py \
  /path/to/staging/.agents \
  --source-root .agents \
  --source-id release-or-commit
```

The destination must not already exist. This prevents an update from silently mixing files from different bundle versions.

For release validation, package into a fresh temporary destination and validate that staged snapshot as well as the canonical source. This catches missing inventory entries, stale generated manifests, and packaging-only path errors before publication.

## Contribution Rules

1. Treat `.agents/` as the canonical source tree.
2. Keep each skill focused on one responsibility.
3. Update a skill's description whenever its trigger or boundary changes.
4. Put shared contracts in `.agents/references/`; keep skill-specific material inside that skill.
5. Run the bundle validator before submitting a change.
6. Rebuild and verify the release manifest for every published snapshot.
7. Smoke-test a freshly packaged snapshot whenever the skill inventory, shared contracts, or packager changes.

## License

GDKP is licensed under the [Apache License 2.0](../LICENSE).
