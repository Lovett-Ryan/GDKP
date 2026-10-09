#!/usr/bin/env python3
"""Validate the structure, metadata, links, and language of this skill bundle."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import unicodedata
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment error
    raise SystemExit("PyYAML is required to validate skill metadata.") from exc


EXPECTED_SKILLS = (
    "knowledge-product-orchestrator",
    "project-workspace-lifecycle",
    "intent-source-analysis",
    "requirement-reconstruction",
    "knowledge-framework",
    "large-publication-architect",
    "zotero-source-gate",
    "notion-node-author",
    "notion-natural-prose-editor",
    "obsidian-knowledge-views",
    "knowledge-base-reuse",
    "knowledge-base-evolution",
    "outcome-orchestrator",
    "domain-skill-acquisition",
)
BUNDLE_VERSION = "1.1.0"

NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".jsonl", ".py"}
REQUIRED_REFERENCES = {
    "citation-and-embed-policy.md",
    "claim-evidence-contract.md",
    "curriculum-coverage-policy.md",
    "domain-capability-gap-policy.md",
    "github-skill-acquisition-policy.md",
    "knowledge-node-relation-schema.md",
    "large-publication-state-contract.md",
    "managed-content-boundaries.md",
    "notion-node-template.md",
    "outcome-profiles.md",
    "project-kernel.md",
    "question-gates.md",
    "requirement-schema.md",
    "reuse-and-evolution-policy.md",
    "scenario-catalog.md",
    "source-policy-by-domain.md",
    "view-projection-policy.md",
    "workflow-contracts.md",
    "zotero-item-normalization.md",
}
INSTALLED_DOMAIN_SKILL_STATUSES = {
    "audited",
    "active",
    "activation_pending",
    "quarantined",
    "disabled",
}


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_digest(files: dict[str, str]) -> str:
    digest = hashlib.sha256()
    for relative, value in sorted(files.items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(value.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def core_inventory(bundle_root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    roots = [bundle_root / "skills" / name for name in EXPECTED_SKILLS]
    roots.extend((bundle_root / "references", bundle_root / "scripts"))
    for root in roots:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            files[path.relative_to(bundle_root).as_posix()] = file_digest(path)
    return files


def validate_core_manifest(bundle_root: Path) -> list[str]:
    manifest_path = bundle_root / "core-bundle-manifest.yaml"
    if not manifest_path.is_file():
        return []
    errors: list[str] = []
    try:
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return [f"core-bundle-manifest.yaml: cannot read manifest: {exc}"]
    if not isinstance(manifest, dict):
        return ["core-bundle-manifest.yaml: manifest must be a mapping"]
    bundle_version = manifest.get("bundle_version")
    if bundle_version != BUNDLE_VERSION:
        errors.append(
            "core-bundle-manifest.yaml: bundle_version must be " + BUNDLE_VERSION
        )
    declared_skill_versions = manifest.get("skill_versions")
    expected_skill_versions = {name: BUNDLE_VERSION for name in EXPECTED_SKILLS}
    if not isinstance(declared_skill_versions, dict) or not all(
        isinstance(name, str) and isinstance(version, str)
        for name, version in declared_skill_versions.items()
    ):
        errors.append(
            "core-bundle-manifest.yaml: skill_versions must map skill names to versions"
        )
    else:
        missing_skill_versions = sorted(
            set(expected_skill_versions) - set(declared_skill_versions)
        )
        unexpected_skill_versions = sorted(
            set(declared_skill_versions) - set(expected_skill_versions)
        )
        mismatched_skill_versions = sorted(
            name
            for name in set(expected_skill_versions) & set(declared_skill_versions)
            if declared_skill_versions[name] != expected_skill_versions[name]
        )
        if missing_skill_versions:
            errors.append(
                "core-bundle-manifest.yaml: missing skill version entries: "
                + ", ".join(missing_skill_versions)
            )
        if unexpected_skill_versions:
            errors.append(
                "core-bundle-manifest.yaml: unexpected skill version entries: "
                + ", ".join(unexpected_skill_versions)
            )
        if mismatched_skill_versions:
            errors.append(
                "core-bundle-manifest.yaml: skill versions must match bundle version for: "
                + ", ".join(mismatched_skill_versions)
            )
    declared_files = manifest.get("files")
    if not isinstance(declared_files, dict) or not all(
        isinstance(path, str) and isinstance(digest, str)
        for path, digest in declared_files.items()
    ):
        return ["core-bundle-manifest.yaml: files must map paths to SHA-256 strings"]
    invalid_digests = sorted(
        path for path, digest in declared_files.items() if not re.fullmatch(r"[0-9a-f]{64}", digest)
    )
    if invalid_digests:
        errors.append(
            "core-bundle-manifest.yaml: invalid file digests: " + ", ".join(invalid_digests)
        )
    actual_files = core_inventory(bundle_root)
    missing_entries = sorted(set(actual_files) - set(declared_files))
    unexpected_entries = sorted(set(declared_files) - set(actual_files))
    if missing_entries:
        errors.append(
            "core-bundle-manifest.yaml: unlisted core files: " + ", ".join(missing_entries)
        )
    if unexpected_entries:
        errors.append(
            "core-bundle-manifest.yaml: non-core or missing files listed: "
            + ", ".join(unexpected_entries)
        )
    for relative in sorted(set(actual_files) & set(declared_files)):
        if actual_files[relative] != declared_files[relative]:
            errors.append(f"core-bundle-manifest.yaml: digest mismatch for {relative}")
    declared_tree = manifest.get("tree_sha256")
    if not isinstance(declared_tree, str) or not re.fullmatch(r"[0-9a-f]{64}", declared_tree):
        errors.append("core-bundle-manifest.yaml: tree_sha256 must be lowercase SHA-256 hex")
    elif not invalid_digests and tree_digest(declared_files) != declared_tree:
        errors.append("core-bundle-manifest.yaml: tree_sha256 does not match files")
    return errors


def governed_domain_skill_names(bundle_root: Path) -> tuple[set[str], list[str]]:
    lock_path = bundle_root.parent / ".knowledge-product" / "domain-skills.lock.yaml"
    if not lock_path.is_file():
        return set(), ["additional project Skills require .knowledge-product/domain-skills.lock.yaml"]
    try:
        data = yaml.safe_load(lock_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return set(), [f"domain-skills.lock.yaml: cannot read lock: {exc}"]
    entries = data.get("domain_skills") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        return set(), ["domain-skills.lock.yaml: domain_skills must be a list"]
    names: set[str] = set()
    errors: list[str] = []
    for index, entry in enumerate(entries):
        naming = entry.get("naming") if isinstance(entry, dict) else None
        name = naming.get("canonical_name") if isinstance(naming, dict) else None
        local_path = naming.get("local_path") if isinstance(naming, dict) else None
        status = entry.get("status") if isinstance(entry, dict) else None
        expected_path = f".agents/skills/{name}" if isinstance(name, str) else None
        if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
            errors.append(f"domain-skills.lock.yaml: entry {index} has invalid canonical_name")
            continue
        if local_path != expected_path:
            errors.append(f"domain-skills.lock.yaml: entry {index} local_path does not match {name}")
            continue
        if status not in INSTALLED_DOMAIN_SKILL_STATUSES:
            continue
        names.add(name)
    return names, errors


def validate_domain_skill(bundle_root: Path, name: str) -> list[str]:
    errors: list[str] = []
    skill_dir = bundle_root / "skills" / name
    skill_md = skill_dir / "SKILL.md"
    ui_file = skill_dir / "agents" / "openai.yaml"
    if not skill_md.is_file() or not ui_file.is_file():
        return [f"{name}: governed domain Skill requires SKILL.md and agents/openai.yaml"]
    try:
        frontmatter = read_frontmatter(skill_md)
        ui = yaml.safe_load(ui_file.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError, yaml.YAMLError) as exc:
        return [f"{name}: invalid governed domain Skill metadata: {exc}"]
    if frontmatter.get("name") != name:
        errors.append(f"{name}: frontmatter name must match the governed directory")
    if not isinstance(frontmatter.get("description"), str) or len(frontmatter["description"].strip()) < 40:
        errors.append(f"{name}: description is missing or not discriminating")
    interface = ui.get("interface") if isinstance(ui, dict) else None
    if not isinstance(interface, dict):
        errors.append(f"{name}: missing interface metadata")
    elif not isinstance(interface.get("default_prompt"), str) or f"${name}" not in interface["default_prompt"]:
        errors.append(f"{name}: default_prompt must mention ${name}")
    return errors
REQUIRED_SCRIPTS = {
    "generate_domain_skill_name.py",
    "package_core_bundle.py",
    "score_domain_skill.py",
    "validate_bundle.py",
    "validate_claim_audit.py",
    "validate_citation_projection.py",
    "validate_coverage_audit.py",
    "validate_handoff.py",
    "validate_large_publication_state.py",
}

CORE_REQUIRED_TEXT = {
    "references/curriculum-coverage-policy.md": (
        "Separate Breadth From Depth",
        "ScopeDecisionLedger",
        "CoverageBaseline",
        "TopicCoverageMatrix",
        "OmissionLedger",
        "Orthogonal Large-Publication Branch",
        "full-book completion barrier",
    ),
    "references/project-kernel.md": (
        "GDKP-<Project Name>",
        "<project-root>/Obsidian/",
        "DraftPacket queue",
        "Runtime compaction",
    ),
    "references/notion-node-template.md": (
        "textbook or monograph",
        "never create a Source View image",
        "DraftPacket",
        "definition + explanation + role/connection",
        "Recommended Reading",
    ),
    "references/view-projection-policy.md": (
        "one curated project knowledge graph",
        "student notes",
    ),
    "references/question-gates.md": (
        "Never show internal YAML",
        "Routine reversible writes",
        "coverage breadth",
        "learning depth",
    ),
    "skills/intent-source-analysis/SKILL.md": (
        "ScopeDecisionLedger",
        "CoverageProfile",
        "broad field remains visible while depth varies by topic",
    ),
    "skills/requirement-reconstruction/SKILL.md": (
        "semantic provenance",
        "CoverageContract",
        "requirements_coverage_complete",
    ),
    "skills/knowledge-framework/SKILL.md": (
        "Coverage-First Design",
        "TopicCoverageMatrix",
        "coverage_unverified",
    ),
    "skills/large-publication-architect/SKILL.md": (
        "FullBookChapterKnowledgeMap",
        "DraftPacket",
        "runtime compaction",
        "exercise_gate: false",
        "model_semantic_review",
        "Single-Pass Pre-Publication Draft Review",
        "No Routine Post-Write Audit",
        "source and factual-claim audit",
    ),
    "skills/zotero-source-gate/SKILL.md": (
        "Structural Coverage Baseline",
        "CoverageBaseline",
        "structural role from factual-evidence role",
        "support_assessment",
        "--evidence-pack",
        "citation-ready Zotero metadata",
    ),
    "skills/knowledge-product-orchestrator/SKILL.md": (
        "Coverage-First Routing",
        "Large-Publication Routing",
        "CoverageAuditReceipt",
        "LargePublicationRunState",
        "validate_large_publication_state.py",
        "gate_receipt",
        "Proportional Audit Path",
        "never send the repaired draft through a second Architect review",
        "Never describe requirement coverage as domain completeness",
        "validate_citation_projection.py",
    ),
    "skills/notion-node-author/SKILL.md": (
        "Single Draft Review, Zotero Audit, and Direct Publication",
        "packet-dispatch",
        "publish-ready",
        "do not reload",
        "CitationProjection",
        "--source-draft",
    ),
    "skills/notion-natural-prose-editor/SKILL.md": (
        "Do not run by default",
    ),
    "skills/obsidian-knowledge-views/SKILL.md": (
        "without rereading notes",
        "Do not create verification receipts",
    ),
    "references/workflow-contracts.md": (
        "FullBookChapterKnowledgeMap",
        "DraftPacket queue",
        "runtime compaction",
        "full-book completion barrier",
        "LargePublicationRunState",
        "validate_large_publication_state.py",
        "one bounded pre-publication Architect DraftQualityReview",
        "never a second Architect review",
    ),
    "references/large-publication-state-contract.md": (
        "LargePublicationRunState",
        "Forward Lifecycle",
        "Prospective Validation Gates",
        "hash-chained receipts",
        "validate_large_publication_state.py",
        "validate_claim_audit.py",
        "validate_citation_projection.py",
    ),
    "references/claim-evidence-contract.md": (
        "locator-specific EvidenceUnits",
        "support_assessment",
        "generic chapter-level EvidenceUnit",
    ),
    "references/citation-and-embed-policy.md": (
        "Citation Projection",
        "validate_citation_projection.py",
        "Recommended Reading",
    ),
}


def read_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---(?:\n|$)", text, re.DOTALL)
    if not match:
        raise ValueError("missing YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data


def validate_skill(bundle_root: Path, name: str) -> list[str]:
    errors: list[str] = []
    skill_dir = bundle_root / "skills" / name
    skill_md = skill_dir / "SKILL.md"
    ui_file = skill_dir / "agents" / "openai.yaml"

    if not skill_md.is_file():
        return [f"{name}: missing SKILL.md"]
    if not ui_file.is_file():
        return [f"{name}: missing agents/openai.yaml"]

    try:
        frontmatter = read_frontmatter(skill_md)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(f"{name}: invalid SKILL.md frontmatter: {exc}")
        return errors

    declared_name = frontmatter.get("name")
    description = frontmatter.get("description")
    if declared_name != name:
        errors.append(f"{name}: frontmatter name is {declared_name!r}")
    if not isinstance(declared_name, str) or not NAME_PATTERN.fullmatch(declared_name):
        errors.append(f"{name}: name must use lowercase letters, digits, and hyphens")
    if isinstance(declared_name, str) and len(declared_name) > 64:
        errors.append(f"{name}: name exceeds 64 characters")
    if not isinstance(description, str) or len(description.strip()) < 40:
        errors.append(f"{name}: description is missing or not discriminating")
    elif len(description) > 1024:
        errors.append(f"{name}: description exceeds 1024 characters")

    try:
        ui = yaml.safe_load(ui_file.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"{name}: invalid agents/openai.yaml: {exc}")
        return errors
    interface = ui.get("interface") if isinstance(ui, dict) else None
    if not isinstance(interface, dict):
        errors.append(f"{name}: missing interface metadata")
        return errors
    display_name = interface.get("display_name")
    short_description = interface.get("short_description")
    default_prompt = interface.get("default_prompt")
    if not isinstance(display_name, str) or not display_name.strip():
        errors.append(f"{name}: missing display_name")
    if not isinstance(short_description, str) or not 25 <= len(short_description) <= 64:
        errors.append(f"{name}: short_description must contain 25-64 characters")
    if not isinstance(default_prompt, str) or f"${name}" not in default_prompt:
        errors.append(f"{name}: default_prompt must mention ${name}")

    skill_text = skill_md.read_text(encoding="utf-8")
    if "../../references/workflow-contracts.md" not in skill_text:
        errors.append(f"{name}: does not link the canonical workflow contract")
    for raw_target in LINK_PATTERN.findall(skill_text):
        target = raw_target.split("#", 1)[0]
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        resolved = (skill_md.parent / target).resolve()
        if bundle_root not in resolved.parents and resolved != bundle_root:
            errors.append(f"{name}: relative link escapes the bundle root: {raw_target!r}")
            continue
        if not resolved.exists():
            errors.append(f"{name}: broken relative link {raw_target!r}")

    return errors


def validate_language(bundle_root: Path) -> list[str]:
    errors: list[str] = []
    paths: list[Path] = []
    readme = bundle_root / "README.md"
    if readme.is_file():
        paths.append(readme)
    for relative_root in ("skills", "references", "scripts", "tests"):
        root = bundle_root / relative_root
        if not root.exists():
            continue
        paths.extend(
            path
            for path in root.rglob("*")
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES
        )
    for path in paths:
        text = path.read_text(encoding="utf-8")
        unfinished_markers = ("[" + "TODO", "TODO" + ":")
        if any(marker in text for marker in unfinished_markers):
            errors.append(f"{path.relative_to(bundle_root)}: unfinished TODO marker")
        if path.suffix.lower() == ".md":
            fence_count = sum(
                1 for line in text.splitlines() if line.lstrip().startswith("```")
            )
            if fence_count % 2:
                errors.append(f"{path.relative_to(bundle_root)}: unbalanced code fences")
        match_index = next(
            (
                index
                for index, character in enumerate(text)
                if unicodedata.category(character).startswith("L")
                and "LATIN" not in unicodedata.name(character, "")
            ),
            None,
        )
        if match_index is not None:
            line = text.count("\n", 0, match_index) + 1
            errors.append(
                f"{path.relative_to(bundle_root)}:{line}: contains a non-English script character"
            )
    return errors


def validate_markdown_links(bundle_root: Path) -> list[str]:
    errors: list[str] = []
    markdown_paths = [bundle_root / "README.md"]
    markdown_paths.extend((bundle_root / "skills").rglob("*.md"))
    markdown_paths.extend((bundle_root / "references").rglob("*.md"))
    for path in markdown_paths:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK_PATTERN.findall(text):
            target = raw_target.split("#", 1)[0].strip().strip("<>")
            if not target or "://" in target or target.startswith("mailto:"):
                continue
            resolved = (path.parent / target).resolve()
            if bundle_root not in resolved.parents and resolved != bundle_root:
                errors.append(
                    f"{path.relative_to(bundle_root)}: relative link escapes bundle root: {raw_target!r}"
                )
            elif not resolved.exists():
                errors.append(
                    f"{path.relative_to(bundle_root)}: broken relative link {raw_target!r}"
                )
    return errors


def validate_core_contract(bundle_root: Path) -> list[str]:
    errors: list[str] = []
    for relative, required_fragments in CORE_REQUIRED_TEXT.items():
        path = bundle_root / relative
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in required_fragments:
            if fragment not in text:
                errors.append(f"{relative}: missing core contract fragment {fragment!r}")
    for name in EXPECTED_SKILLS:
        ui_path = bundle_root / "skills" / name / "agents" / "openai.yaml"
        if not ui_path.is_file():
            continue
        try:
            ui = yaml.safe_load(ui_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError):
            continue
        interface = ui.get("interface") if isinstance(ui, dict) else None
        display_name = interface.get("display_name") if isinstance(interface, dict) else None
        if not isinstance(display_name, str) or not display_name.startswith("GDKP-"):
            errors.append(f"{name}: display_name must start with 'GDKP-'")
    retired_helper = bundle_root / "scripts" / "compute_center_score.py"
    if retired_helper.exists():
        errors.append("scripts/compute_center_score.py is retired")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "bundle_root",
        nargs="?",
        default=Path(__file__).resolve().parents[1],
        type=Path,
    )
    args = parser.parse_args()
    bundle_root = args.bundle_root.resolve()

    errors: list[str] = []
    skills_root = bundle_root / "skills"
    if not skills_root.is_dir():
        print("ERROR: missing skills directory", file=sys.stderr)
        return 1
    actual = {
        path.name
        for path in skills_root.iterdir()
        if path.is_dir()
    }
    missing = sorted(set(EXPECTED_SKILLS) - actual)
    additional = sorted(actual - set(EXPECTED_SKILLS))
    if missing:
        errors.append(f"missing skill directories: {', '.join(missing)}")
    if additional:
        governed, lock_errors = governed_domain_skill_names(bundle_root)
        errors.extend(lock_errors)
        unmanaged = sorted(set(additional) - governed)
        if unmanaged:
            errors.append(f"ungoverned project skill directories: {', '.join(unmanaged)}")
        for skill_name in sorted(set(additional) & governed):
            errors.extend(validate_domain_skill(bundle_root, skill_name))

    references_root = bundle_root / "references"
    actual_references = (
        {path.name for path in references_root.iterdir() if path.is_file()}
        if references_root.is_dir()
        else set()
    )
    missing_references = sorted(REQUIRED_REFERENCES - actual_references)
    if missing_references:
        errors.append(f"missing shared references: {', '.join(missing_references)}")

    scripts_root = bundle_root / "scripts"
    actual_scripts = (
        {path.name for path in scripts_root.iterdir() if path.is_file()}
        if scripts_root.is_dir()
        else set()
    )
    missing_scripts = sorted(REQUIRED_SCRIPTS - actual_scripts)
    if missing_scripts:
        errors.append(f"missing deterministic scripts: {', '.join(missing_scripts)}")

    for skill_name in EXPECTED_SKILLS:
        errors.extend(validate_skill(bundle_root, skill_name))
    errors.extend(validate_core_manifest(bundle_root))
    errors.extend(validate_language(bundle_root))
    errors.extend(validate_markdown_links(bundle_root))
    errors.extend(validate_core_contract(bundle_root))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Validated {len(EXPECTED_SKILLS)} skills with no structural or language errors.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
