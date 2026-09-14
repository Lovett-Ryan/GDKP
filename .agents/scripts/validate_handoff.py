#!/usr/bin/env python3
"""Validate a JSON or YAML workflow handoff envelope."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import re
import sys
from pathlib import Path


MODES = {"knowledge", "product", "hybrid"}
STAGES = {
    "draft",
    "setup",
    "initialized",
    "brief_confirmed",
    "sources_confirmed",
    "reuse_review",
    "evolution_review",
    "composing",
    "published",
    "publication_verified",
    "graph_stale",
    "graph_updated",
    "executing",
    "validating",
    "completed",
    "capability_gap_detected",
    "skill_candidate_review",
    "skill_staging",
    "skill_audit",
    "capability_ready",
    "capability_fallback",
    "quarantined",
    "resume_originating_stage",
}
STATUSES = {
    "ready",
    "needs_question",
    "needs_approval",
    "needs_replan",
    "blocked",
    "paused",
    "completed",
}
CORE_SKILLS = {
    "knowledge-product-orchestrator",
    "project-workspace-lifecycle",
    "intent-source-analysis",
    "requirement-reconstruction",
    "knowledge-framework",
    "zotero-source-gate",
    "notion-node-author",
    "notion-natural-prose-editor",
    "obsidian-knowledge-views",
    "knowledge-base-reuse",
    "knowledge-base-evolution",
    "outcome-orchestrator",
    "domain-skill-acquisition",
}
ARTIFACT_STATUSES = {
    "draft",
    "pending",
    "approved",
    "verified",
    "current",
    "admitted",
    "published",
    "active",
    "completed",
    "rejected",
    "superseded",
    "invalidated",
    "quarantined",
}
ARTIFACT_OWNERS = {
    "ProjectContext": "project-workspace-lifecycle",
    "CapabilityReport": "project-workspace-lifecycle",
    "DomainSkillRegistry": "project-workspace-lifecycle",
    "IntentContract": "intent-source-analysis",
    "SourcePolicy": "intent-source-analysis",
    "RequirementContract": "requirement-reconstruction",
    "GoalContract": "requirement-reconstruction",
    "WorkPackageGraph": "requirement-reconstruction",
    "FrameworkSpec": "knowledge-framework",
    "ContainerRegistry": "knowledge-framework",
    "KnowledgeNodeRegistry": "knowledge-framework",
    "RelationRegistry": "knowledge-framework",
    "ClaimIntentBundle": "knowledge-framework",
    "SourceGapReport": "knowledge-framework",
    "FrameworkDiff": "knowledge-framework",
    "CandidateManifest": "zotero-source-gate",
    "EvidencePack": "zotero-source-gate",
    "SourceAuditReport": "zotero-source-gate",
    "ClaimAuditReceipt": "zotero-source-gate",
    "DraftClaimSet": "notion-node-author",
    "ClaimAuditRequest": "notion-node-author",
    "NotionPublicationPack": "notion-node-author",
    "NaturalProseRevisionMemo": "notion-natural-prose-editor",
    "GraphPlan": "obsidian-knowledge-views",
    "KnowledgeGraphManifest": "obsidian-knowledge-views",
    "ReuseCandidateManifest": "knowledge-base-reuse",
    "ReuseLineage": "knowledge-base-reuse",
    "EvolutionChangeSet": "knowledge-base-evolution",
    "TaskSpec": "outcome-orchestrator",
    "TaskGraph": "outcome-orchestrator",
    "OutcomeEvidence": "outcome-orchestrator",
    "DomainSkillCandidateManifest": "domain-skill-acquisition",
    "DomainSkillLockEntry": "domain-skill-acquisition",
    "DomainSkillReceipt": "domain-skill-acquisition",
    "DomainSkillInvocationAuthorization": "knowledge-product-orchestrator",
    "DomainSkillInvocationReceipt": "knowledge-product-orchestrator",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SKILL_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
UUID7_BODY = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
REQUIRED = {
    "schema_version",
    "project_id",
    "run_id",
    "producer_skill",
    "created_at",
    "mode",
    "stage",
    "status",
    "input_refs",
    "artifacts",
    "decisions",
    "unresolved_questions",
    "proposed_mutations",
    "input_versions",
    "artifact_schema_versions",
    "approval_ids",
    "binding_revision",
    "checkpoint_id",
    "op_ids",
    "receipts",
    "next_skill",
}


def require_nonempty_string(envelope: dict, key: str, errors: list[str]) -> None:
    value = envelope.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{key} must be a non-empty string")


def validate_timestamp(value: object) -> bool:
    if not isinstance(value, str) or not value.endswith(("Z", "+00:00")):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def valid_skill_name(value: object) -> bool:
    return isinstance(value, str) and len(value) <= 64 and bool(SKILL_NAME.fullmatch(value))


def valid_prefixed_uuid7(value: object, prefix: str) -> bool:
    return (
        isinstance(value, str)
        and value.startswith(prefix)
        and bool(UUID7_BODY.fullmatch(value[len(prefix) :]))
    )


def load_document(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        data = json.loads(text)
    else:
        try:
            import yaml
        except ImportError as exc:
            raise ValueError("PyYAML is required for YAML input") from exc
        data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError("document root must be a mapping")
    return data


def validate(data: dict) -> list[str]:
    envelope = data.get("handoff", data)
    if not isinstance(envelope, dict):
        return ["handoff must be a mapping"]
    errors = [f"missing field: {key}" for key in sorted(REQUIRED - envelope.keys())]
    if errors:
        return errors

    if not isinstance(envelope["schema_version"], int) or isinstance(
        envelope["schema_version"], bool
    ) or envelope["schema_version"] != 1:
        errors.append("schema_version must be 1")
    for field in ("project_id", "run_id", "stage", "checkpoint_id"):
        require_nonempty_string(envelope, field, errors)
    if not valid_prefixed_uuid7(envelope.get("project_id"), "prj_"):
        errors.append("project_id must be prj_<UUIDv7>")
    if not valid_prefixed_uuid7(envelope.get("run_id"), "run_"):
        errors.append("run_id must be run_<UUIDv7>")
    if not valid_prefixed_uuid7(envelope.get("checkpoint_id"), "chk_"):
        errors.append("checkpoint_id must be chk_<UUIDv7>")
    if not validate_timestamp(envelope.get("created_at")):
        errors.append("created_at must be an RFC 3339 UTC timestamp")
    if not isinstance(envelope["mode"], str) or envelope["mode"] not in MODES:
        errors.append(f"invalid mode: {envelope['mode']!r}")
    if not isinstance(envelope["stage"], str) or envelope["stage"] not in STAGES:
        errors.append(f"invalid stage: {envelope['stage']!r}")
    if not isinstance(envelope["status"], str) or envelope["status"] not in STATUSES:
        errors.append(f"invalid status: {envelope['status']!r}")
    if not valid_skill_name(envelope["producer_skill"]):
        errors.append(f"invalid producer_skill name: {envelope['producer_skill']!r}")
    if envelope["next_skill"] is not None and not valid_skill_name(envelope["next_skill"]):
        errors.append(f"invalid next_skill name: {envelope['next_skill']!r}")
    if not isinstance(envelope["binding_revision"], int) or isinstance(
        envelope["binding_revision"], bool
    ) or envelope["binding_revision"] < 1:
        errors.append("binding_revision must be a positive integer")

    list_fields = (
        "input_refs",
        "artifacts",
        "decisions",
        "unresolved_questions",
        "proposed_mutations",
        "approval_ids",
        "op_ids",
        "receipts",
    )
    for field in list_fields:
        if not isinstance(envelope[field], list):
            errors.append(f"{field} must be a list")
    for field in ("approval_ids", "op_ids"):
        values = envelope.get(field)
        if isinstance(values, list) and not all(
            isinstance(value, str) and value.strip() for value in values
        ):
            errors.append(f"{field} must contain non-empty strings")
        if (
            isinstance(values, list)
            and all(isinstance(value, str) for value in values)
            and len(values) != len(set(values))
        ):
            errors.append(f"{field} must not contain duplicates")
    for field in ("input_versions", "artifact_schema_versions"):
        if not isinstance(envelope[field], dict):
            errors.append(f"{field} must be a mapping")

    if isinstance(envelope["artifacts"], list):
        artifact_ids: list[str] = []
        for index, artifact in enumerate(envelope["artifacts"]):
            if not isinstance(artifact, dict):
                errors.append(f"artifacts[{index}] must be a mapping")
                continue
            for key in (
                "artifact_type",
                "artifact_id",
                "uri",
                "revision",
                "schema_version",
                "sha256",
                "producer_skill",
                "status",
            ):
                if key not in artifact:
                    errors.append(f"artifacts[{index}] is missing {key}")
            digest = artifact.get("sha256")
            if digest is not None and (not isinstance(digest, str) or not SHA256.fullmatch(digest)):
                errors.append(f"artifacts[{index}].sha256 must be lowercase SHA-256 hex")
            producer = artifact.get("producer_skill")
            if producer is not None and not valid_skill_name(producer):
                errors.append(f"artifacts[{index}] has an invalid producer_skill")
            for key in ("artifact_type", "artifact_id", "uri", "status"):
                value = artifact.get(key)
                if value is not None and (not isinstance(value, str) or not value.strip()):
                    errors.append(f"artifacts[{index}].{key} must be a non-empty string")
            for key in ("revision", "schema_version"):
                value = artifact.get(key)
                if value is not None and (
                    not isinstance(value, int) or isinstance(value, bool) or value < 1
                ):
                    errors.append(f"artifacts[{index}].{key} must be a positive integer")
            artifact_id = artifact.get("artifact_id")
            if isinstance(artifact_id, str):
                artifact_ids.append(artifact_id)
            artifact_type = artifact.get("artifact_type")
            status = artifact.get("status")
            if isinstance(status, str) and status not in ARTIFACT_STATUSES:
                errors.append(f"artifacts[{index}] has an invalid artifact status")
            expected_owner = ARTIFACT_OWNERS.get(artifact_type) if isinstance(artifact_type, str) else None
            if expected_owner is not None and producer != expected_owner:
                errors.append(
                    f"artifacts[{index}] {artifact_type} must be produced by {expected_owner}"
                )
            schema_versions = envelope.get("artifact_schema_versions")
            if (
                isinstance(artifact_type, str)
                and isinstance(schema_versions, dict)
                and artifact_type in schema_versions
                and artifact.get("schema_version") != schema_versions[artifact_type]
            ):
                errors.append(
                    f"artifacts[{index}].schema_version disagrees with artifact_schema_versions"
                )
        if len(artifact_ids) != len(set(artifact_ids)):
            errors.append("artifact_id values must be unique")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path)
    args = parser.parse_args()
    try:
        data = load_document(args.document)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Handoff envelope is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
