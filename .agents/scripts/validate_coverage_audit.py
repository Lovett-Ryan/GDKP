#!/usr/bin/env python3
"""Validate scope provenance and broad-domain curriculum coverage artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys


TRANSFORMATIONS = {"preserve", "expand", "narrow", "exclude", "infer"}
AUTHORITIES = {"user", "policy", "structural_evidence", "ai"}
BREADTHS = {
    "focused",
    "canonical_foundations",
    "broad_field_map",
    "reference_comprehensive",
}
IMPORTANCE = {"core", "important", "specialized"}
DISPOSITIONS = {"mastery", "understanding", "awareness", "deferred", "excluded"}
INCLUDED_DISPOSITIONS = {"mastery", "understanding", "awareness"}
OMITTED_DISPOSITIONS = {"deferred", "excluded"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def require_object(value: object, label: str, errors: list[str]) -> dict:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return {}
    return value


def require_list(value: object, label: str, errors: list[str]) -> list:
    if not isinstance(value, list):
        errors.append(f"{label} must be a list")
        return []
    return value


def duplicate_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def find_dependency_cycle(dependencies: dict[str, list[str]]) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()
    path: list[str] = []

    def visit(topic_id: str) -> list[str] | None:
        if topic_id in visiting:
            start = path.index(topic_id)
            return path[start:] + [topic_id]
        if topic_id in visited:
            return None
        visiting.add(topic_id)
        path.append(topic_id)
        for dependency_id in dependencies.get(topic_id, []):
            cycle = visit(dependency_id)
            if cycle:
                return cycle
        path.pop()
        visiting.remove(topic_id)
        visited.add(topic_id)
        return None

    for topic_id in dependencies:
        cycle = visit(topic_id)
        if cycle:
            return cycle
    return None


def validate(payload: object) -> tuple[list[str], dict[str, object]]:
    errors: list[str] = []
    root = require_object(payload, "document", errors)
    audit = require_object(root.get("coverage_audit"), "coverage_audit", errors)
    project_id = audit.get("project_id")
    if not is_nonempty_string(project_id):
        errors.append("coverage_audit.project_id must be a non-empty string")

    profile = require_object(audit.get("coverage_profile"), "coverage_profile", errors)
    if profile.get("mode") != "coverage_first":
        errors.append("coverage_profile.mode must be coverage_first")
    if profile.get("breadth") not in BREADTHS:
        errors.append("coverage_profile.breadth is invalid")

    decisions = require_list(audit.get("scope_decisions"), "scope_decisions", errors)
    decision_ids: list[str] = []
    for index, item in enumerate(decisions):
        decision = require_object(item, f"scope_decisions[{index}]", errors)
        decision_id = decision.get("decision_id")
        if not is_nonempty_string(decision_id):
            errors.append(f"scope_decisions[{index}].decision_id must be non-empty")
        else:
            decision_ids.append(decision_id)
        if not is_nonempty_string(decision.get("raw_fragment_ref")):
            errors.append(f"scope_decisions[{index}].raw_fragment_ref must be non-empty")
        if not is_nonempty_string(decision.get("normalized_clause")):
            errors.append(f"scope_decisions[{index}].normalized_clause must be non-empty")
        transformation = decision.get("transformation")
        if transformation not in TRANSFORMATIONS:
            errors.append(f"scope_decisions[{index}].transformation is invalid")
        authority = require_object(
            decision.get("authority"), f"scope_decisions[{index}].authority", errors
        )
        authority_kind = authority.get("kind")
        if authority_kind not in AUTHORITIES:
            errors.append(f"scope_decisions[{index}].authority.kind is invalid")
        if transformation in {"narrow", "exclude"}:
            if authority_kind == "ai":
                errors.append(
                    f"scope_decisions[{index}] silently narrows scope with AI authority"
                )
            if not is_nonempty_string(authority.get("ref")):
                errors.append(
                    f"scope_decisions[{index}] narrowing requires an authority reference"
                )
    for duplicate in duplicate_values(decision_ids):
        errors.append(f"duplicate scope decision_id: {duplicate}")

    baseline = require_object(audit.get("baseline"), "baseline", errors)
    baseline_id = baseline.get("baseline_id")
    if not is_nonempty_string(baseline_id):
        errors.append("baseline.baseline_id must be a non-empty string")
    if baseline.get("project_id") != project_id:
        errors.append("baseline.project_id does not match coverage_audit.project_id")
    sources = require_list(baseline.get("sources"), "baseline.sources", errors)
    source_ids: list[str] = []
    local_source_count = 0
    for index, item in enumerate(sources):
        source = require_object(item, f"baseline.sources[{index}]", errors)
        source_id = source.get("source_id")
        if not is_nonempty_string(source_id):
            errors.append(f"baseline.sources[{index}].source_id must be non-empty")
        else:
            source_ids.append(source_id)
        if source.get("role") != "structural_baseline":
            errors.append(f"baseline.sources[{index}].role must be structural_baseline")
        source_status = source.get("status")
        if source_status not in {"admitted", "verified", "local_files_verified"}:
            errors.append(
                f"baseline.sources[{index}].status must be admitted, verified, or local_files_verified"
            )
        if source_status == "local_files_verified":
            local_source_count += 1
            for field in ("location_ref", "extraction_method"):
                if not is_nonempty_string(source.get(field)):
                    errors.append(
                        f"baseline.sources[{index}].{field} must be non-empty for local_files_verified"
                    )
            if not isinstance(source.get("content_sha256"), str) or not SHA256_RE.fullmatch(
                source["content_sha256"]
            ):
                errors.append(
                    f"baseline.sources[{index}].content_sha256 must be a lowercase SHA-256 for local_files_verified"
                )
            if source.get("readback_verified") is not True:
                errors.append(
                    f"baseline.sources[{index}].readback_verified must be true for local_files_verified"
                )
            authorization = require_object(
                source.get("authorization"),
                f"baseline.sources[{index}].authorization",
                errors,
            )
            if authorization.get("kind") != "user":
                errors.append(
                    f"baseline.sources[{index}].authorization.kind must be user for local_files_verified"
                )
            if not is_nonempty_string(authorization.get("ref")):
                errors.append(
                    f"baseline.sources[{index}].authorization.ref must be non-empty for local_files_verified"
                )
    for duplicate in duplicate_values(source_ids):
        errors.append(f"duplicate baseline source_id: {duplicate}")

    topics = require_list(baseline.get("topics"), "baseline.topics", errors)
    topic_ids: list[str] = []
    dependencies: dict[str, list[str]] = {}
    topic_importance: dict[str, str] = {}
    for index, item in enumerate(topics):
        topic = require_object(item, f"baseline.topics[{index}]", errors)
        topic_id = topic.get("topic_id")
        if not is_nonempty_string(topic_id):
            errors.append(f"baseline.topics[{index}].topic_id must be non-empty")
            continue
        topic_ids.append(topic_id)
        if not is_nonempty_string(topic.get("title")):
            errors.append(f"baseline.topics[{index}].title must be non-empty")
        importance = topic.get("importance")
        if importance not in IMPORTANCE:
            errors.append(f"baseline.topics[{index}].importance is invalid")
        else:
            topic_importance[topic_id] = importance
        raw_dependencies = require_list(
            topic.get("dependency_ids", []),
            f"baseline.topics[{index}].dependency_ids",
            errors,
        )
        clean_dependencies = [
            value for value in raw_dependencies if is_nonempty_string(value)
        ]
        if len(clean_dependencies) != len(raw_dependencies):
            errors.append(
                f"baseline.topics[{index}].dependency_ids must contain strings"
            )
        dependencies[topic_id] = clean_dependencies
    for duplicate in duplicate_values(topic_ids):
        errors.append(f"duplicate baseline topic_id: {duplicate}")
    topic_id_set = set(topic_ids)
    for topic_id, dependency_ids in dependencies.items():
        for dependency_id in dependency_ids:
            if dependency_id not in topic_id_set:
                errors.append(f"topic {topic_id} has unknown dependency {dependency_id}")
            if dependency_id == topic_id:
                errors.append(f"topic {topic_id} depends on itself")
    cycle = find_dependency_cycle(dependencies)
    if cycle:
        errors.append("baseline topic dependency cycle: " + " -> ".join(cycle))

    contract = require_object(audit.get("coverage_contract"), "coverage_contract", errors)
    if contract.get("project_id") != project_id:
        errors.append("coverage_contract.project_id does not match coverage_audit.project_id")
    if contract.get("baseline_id") != baseline_id:
        errors.append("coverage_contract.baseline_id does not match baseline.baseline_id")
    if contract.get("breadth") != profile.get("breadth"):
        errors.append("coverage_contract.breadth does not match coverage_profile.breadth")
    if not is_nonempty_string(contract.get("completeness_definition")):
        errors.append("coverage_contract.completeness_definition must be non-empty")
    if contract.get("status") != "confirmed":
        errors.append("coverage_contract.status must be confirmed")

    matrix = require_object(audit.get("matrix"), "matrix", errors)
    if matrix.get("project_id") != project_id:
        errors.append("matrix.project_id does not match coverage_audit.project_id")
    if matrix.get("baseline_id") != baseline_id:
        errors.append("matrix.baseline_id does not match baseline.baseline_id")
    mappings = require_list(matrix.get("mappings"), "matrix.mappings", errors)
    mapping_ids: list[str] = []
    mapping_by_topic: dict[str, dict] = {}
    for index, item in enumerate(mappings):
        mapping = require_object(item, f"matrix.mappings[{index}]", errors)
        topic_id = mapping.get("topic_id")
        if not is_nonempty_string(topic_id):
            errors.append(f"matrix.mappings[{index}].topic_id must be non-empty")
            continue
        mapping_ids.append(topic_id)
        mapping_by_topic[topic_id] = mapping
        disposition = mapping.get("disposition")
        if disposition not in DISPOSITIONS:
            errors.append(f"matrix.mappings[{index}].disposition is invalid")
            continue
        targets = require_list(
            mapping.get("target_refs", []),
            f"matrix.mappings[{index}].target_refs",
            errors,
        )
        if not all(is_nonempty_string(target) for target in targets):
            errors.append(f"matrix.mappings[{index}].target_refs must contain strings")
        omission_id = mapping.get("omission_id")
        if disposition in INCLUDED_DISPOSITIONS:
            if not targets:
                errors.append(
                    f"included topic {topic_id} requires at least one framework target"
                )
            if omission_id not in {None, ""}:
                errors.append(f"included topic {topic_id} must not have omission_id")
        elif disposition in OMITTED_DISPOSITIONS:
            if targets:
                errors.append(f"omitted topic {topic_id} must not have target_refs")
            if not is_nonempty_string(omission_id):
                errors.append(f"omitted topic {topic_id} requires omission_id")
    for duplicate in duplicate_values(mapping_ids):
        errors.append(f"duplicate matrix topic_id: {duplicate}")
    missing_mappings = sorted(topic_id_set - set(mapping_ids))
    extra_mappings = sorted(set(mapping_ids) - topic_id_set)
    if missing_mappings:
        errors.append("baseline topics missing from matrix: " + ", ".join(missing_mappings))
    if extra_mappings:
        errors.append("matrix contains unknown topics: " + ", ".join(extra_mappings))

    ledger = require_object(audit.get("omission_ledger"), "omission_ledger", errors)
    if ledger.get("project_id") != project_id:
        errors.append("omission_ledger.project_id does not match coverage_audit.project_id")
    if ledger.get("baseline_id") != baseline_id:
        errors.append("omission_ledger.baseline_id does not match baseline.baseline_id")
    omissions = require_list(ledger.get("omissions"), "omission_ledger.omissions", errors)
    omission_ids: list[str] = []
    omission_by_id: dict[str, dict] = {}
    omission_topics: list[str] = []
    for index, item in enumerate(omissions):
        omission = require_object(item, f"omission_ledger.omissions[{index}]", errors)
        omission_id = omission.get("omission_id")
        topic_id = omission.get("topic_id")
        if not is_nonempty_string(omission_id):
            errors.append(f"omission_ledger.omissions[{index}].omission_id must be non-empty")
        else:
            omission_ids.append(omission_id)
            omission_by_id[omission_id] = omission
        if not is_nonempty_string(topic_id):
            errors.append(f"omission_ledger.omissions[{index}].topic_id must be non-empty")
        else:
            omission_topics.append(topic_id)
        if omission.get("disposition") not in OMITTED_DISPOSITIONS:
            errors.append(f"omission_ledger.omissions[{index}].disposition is invalid")
        for field in ("reason", "learner_impact", "future_route"):
            if not is_nonempty_string(omission.get(field)):
                errors.append(
                    f"omission_ledger.omissions[{index}].{field} must be non-empty"
                )
        authority = require_object(
            omission.get("authority"),
            f"omission_ledger.omissions[{index}].authority",
            errors,
        )
        if authority.get("kind") not in {"user", "policy", "structural_evidence"}:
            errors.append(
                f"omission_ledger.omissions[{index}] requires user, policy, or structural_evidence authority"
            )
        if not is_nonempty_string(authority.get("ref")):
            errors.append(
                f"omission_ledger.omissions[{index}].authority.ref must be non-empty"
            )
    for duplicate in duplicate_values(omission_ids):
        errors.append(f"duplicate omission_id: {duplicate}")
    for duplicate in duplicate_values(omission_topics):
        errors.append(f"duplicate omission topic_id: {duplicate}")

    referenced_omissions: set[str] = set()
    for topic_id, mapping in mapping_by_topic.items():
        disposition = mapping.get("disposition")
        if disposition not in OMITTED_DISPOSITIONS:
            continue
        omission_id = mapping.get("omission_id")
        if is_nonempty_string(omission_id):
            referenced_omissions.add(omission_id)
            omission = omission_by_id.get(omission_id)
            if omission is None:
                errors.append(f"topic {topic_id} references unknown omission {omission_id}")
            else:
                if omission.get("topic_id") != topic_id:
                    errors.append(f"omission {omission_id} does not match topic {topic_id}")
                if omission.get("disposition") != disposition:
                    errors.append(
                        f"omission {omission_id} disposition does not match topic {topic_id}"
                    )
    unused_omissions = sorted(set(omission_by_id) - referenced_omissions)
    if unused_omissions:
        errors.append("unreferenced omissions: " + ", ".join(unused_omissions))

    for topic_id, mapping in mapping_by_topic.items():
        if mapping.get("disposition") not in {"mastery", "understanding"}:
            continue
        blocked_dependencies = [
            dependency_id
            for dependency_id in dependencies.get(topic_id, [])
            if mapping_by_topic.get(dependency_id, {}).get("disposition")
            in OMITTED_DISPOSITIONS
        ]
        if blocked_dependencies and not is_nonempty_string(mapping.get("dependency_limit")):
            errors.append(
                f"topic {topic_id} requires dependency_limit because prerequisites are omitted: "
                + ", ".join(blocked_dependencies)
            )

    status = audit.get("status")
    if status not in {
        "coverage_unverified",
        "coverage_local_verified",
        "coverage_verified",
    }:
        errors.append("coverage_audit.status is invalid")
    if status == "coverage_verified":
        if baseline.get("status") != "verified":
            errors.append("coverage_verified requires baseline.status verified")
        if local_source_count:
            errors.append("coverage_verified cannot rely on local_files_verified sources")
        if not sources:
            errors.append("coverage_verified requires at least one structural source")
        if not topics:
            errors.append("coverage_verified requires at least one baseline topic")
    if status == "coverage_local_verified":
        if baseline.get("status") != "local_files_verified":
            errors.append(
                "coverage_local_verified requires baseline.status local_files_verified"
            )
        if local_source_count < 1:
            errors.append(
                "coverage_local_verified requires at least one local_files_verified source"
            )
        if not topics:
            errors.append(
                "coverage_local_verified requires at least one baseline topic"
            )

    summary: dict[str, object] = {
        "project_id": project_id,
        "baseline_id": baseline_id,
        "status": status,
        "source_count": len(sources),
        "local_source_count": local_source_count,
        "topic_count": len(topics),
        "mapped_topic_count": len(set(mapping_ids) & topic_id_set),
        "omission_count": len(omissions),
        "dependency_cycle": cycle,
        "valid": not errors,
    }
    return errors, summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="JSON document containing coverage_audit")
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read coverage audit: {exc}", file=sys.stderr)
        return 2
    errors, summary = validate(payload)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Coverage audit failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
