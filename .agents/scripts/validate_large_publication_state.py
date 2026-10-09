#!/usr/bin/env python3
"""Validate GDKP large-publication forward state and prospective gates."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


SHA256 = re.compile(r"^[0-9a-f]{64}$")
MODES = {"new_publication", "existing_publication_revision"}
RUN_STATUSES = {
    "mapped",
    "authoring",
    "reviewing",
    "auditing",
    "publishing",
    "complete",
    "invalidated",
}
PACKET_STATUSES = {"queued", "dispatched", "checkpointed", "accepted", "stale"}
UNIT_STATUSES = {
    "planned",
    "assembled",
    "reviewed",
    "resolved",
    "audited",
    "published",
    "stale",
}
SCOPE_BASES = {"obligation_cluster", "argument_stage", "context_split", "continuation"}
FINDING_CATEGORIES = {
    "omission",
    "under_explained",
    "broken_relationship",
    "incorrect_connection",
}
DISPOSITIONS = {"repaired", "governed_exception"}
PASSING_AUDITS = {"passed", "passed_with_caveat"}
GATES = {
    "map-ready",
    "packet-dispatch",
    "packet-checkpoint",
    "review-ready",
    "review-recorded",
    "claim-audit-ready",
    "publish-ready",
    "complete",
}
FORBIDDEN_NEW_MAP_INPUT_TYPES = {
    "draftclaimset",
    "draftpacketcheckpoint",
    "fullbooksnapshot",
    "notionpublicationpack",
    "publicationcoverageindex",
    "readerfacingdraft",
}


def load_state(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("document root must be an object")
    state = data.get("large_publication_run_state", data)
    if not isinstance(state, dict):
        raise ValueError("large_publication_run_state must be an object")
    return state


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def string_list(value: Any) -> bool:
    return isinstance(value, list) and all(nonempty_string(item) for item in value)


def unique_string_list(value: Any) -> bool:
    return string_list(value) and len(value) == len(set(value))


def parse_time(value: Any, label: str, errors: list[str]) -> datetime | None:
    if not nonempty_string(value):
        errors.append(f"{label} must be a non-empty ISO-8601 timestamp")
        return None
    raw = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        errors.append(f"{label} must be a valid ISO-8601 timestamp")
        return None
    if parsed.tzinfo is None:
        errors.append(f"{label} must include a timezone")
        return None
    return parsed


def require_sha(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not SHA256.fullmatch(value):
        errors.append(f"{label} must be lowercase SHA-256 hex")


def normalized_artifact_type(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def compute_state_hash(state: dict[str, Any]) -> str:
    encoded = json.dumps(
        state, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def compute_receipt_hash(receipt: dict[str, Any]) -> str:
    payload = {key: value for key, value in receipt.items() if key != "receipt_sha256"}
    encoded = json.dumps(
        payload, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def receipt_subject(gate: str, packet_id: Any, unit_id: Any) -> str | None:
    if gate in {"packet-dispatch", "packet-checkpoint"}:
        return packet_id if nonempty_string(packet_id) else None
    if gate in {
        "review-ready",
        "review-recorded",
        "claim-audit-ready",
        "publish-ready",
    }:
        return unit_id if nonempty_string(unit_id) else None
    return None


def validate_gate_receipts(
    state: dict[str, Any], errors: list[str], snapshot_root: Path | None
) -> dict[tuple[str, str | None], datetime]:
    if "gate_receipts" not in state:
        errors.append("gate_receipts must be present, using an empty list before the first gate")
    receipts = state.get("gate_receipts", [])
    if not isinstance(receipts, list) or not all(isinstance(item, dict) for item in receipts):
        errors.append("gate_receipts must be an object list")
        return {}
    index: dict[tuple[str, str | None], datetime] = {}
    previous_hash: str | None = None
    previous_time: datetime | None = None
    for position, receipt in enumerate(receipts, start=1):
        label = f"gate_receipts[{position - 1}]"
        if receipt.get("sequence") != position:
            errors.append(f"{label}.sequence must be {position}")
        gate = receipt.get("gate")
        if gate not in GATES - {"complete"}:
            errors.append(f"{label}.gate is not a stored prospective gate")
            continue
        packet_id = receipt.get("packet_id")
        unit_id = receipt.get("unit_id")
        subject = receipt_subject(gate, packet_id, unit_id)
        if gate in {"packet-dispatch", "packet-checkpoint"}:
            if subject is None or unit_id is not None:
                errors.append(f"{label} requires only packet_id")
        elif gate in {
            "review-ready",
            "review-recorded",
            "claim-audit-ready",
            "publish-ready",
        }:
            if subject is None or packet_id is not None:
                errors.append(f"{label} requires only unit_id")
        elif packet_id is not None or unit_id is not None:
            errors.append(f"{label} must not declare a Packet or unit selector")
        key = (gate, subject)
        if key in index:
            errors.append(f"{label} duplicates stored prospective gate {gate} for {subject}")
        checked_at = parse_time(receipt.get("checked_at"), f"{label}.checked_at", errors)
        if checked_at:
            index[key] = checked_at
            if previous_time and checked_at < previous_time:
                errors.append(f"{label}.checked_at predates the previous gate receipt")
            previous_time = checked_at
        require_sha(receipt.get("validated_state_sha256"), f"{label}.validated_state_sha256", errors)
        snapshot_ref = receipt.get("state_snapshot_ref")
        if not nonempty_string(snapshot_ref):
            errors.append(f"{label}.state_snapshot_ref must be a non-empty string")
        elif snapshot_root is None:
            errors.append(f"{label} requires --snapshot-root for historical verification")
        else:
            root = snapshot_root.resolve()
            snapshot_path = (root / snapshot_ref).resolve()
            try:
                snapshot_path.relative_to(root)
            except ValueError:
                errors.append(f"{label}.state_snapshot_ref escapes snapshot root")
            else:
                try:
                    snapshot_state = load_state(snapshot_path)
                except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
                    errors.append(f"{label} cannot read state snapshot: {exc}")
                else:
                    if compute_state_hash(snapshot_state) != receipt.get(
                        "validated_state_sha256"
                    ):
                        errors.append(f"{label} state snapshot does not match its validated hash")
                    if snapshot_state.get("project_id") != state.get("project_id") or snapshot_state.get(
                        "run_id"
                    ) != state.get("run_id"):
                        errors.append(f"{label} state snapshot belongs to another project or run")
                    snapshot_receipts = snapshot_state.get("gate_receipts", [])
                    if snapshot_receipts != receipts[: position - 1]:
                        errors.append(f"{label} state snapshot does not contain the prior receipt chain")
                    gate_errors = validate_gate(snapshot_state, gate, packet_id, unit_id)
                    if gate_errors:
                        errors.append(
                            f"{label} historical snapshot did not satisfy its gate: "
                            + "; ".join(gate_errors)
                        )
        if receipt.get("previous_receipt_sha256") != previous_hash:
            errors.append(f"{label}.previous_receipt_sha256 breaks the receipt chain")
        declared_hash = receipt.get("receipt_sha256")
        require_sha(declared_hash, f"{label}.receipt_sha256", errors)
        computed_hash = compute_receipt_hash(receipt)
        if declared_hash != computed_hash:
            errors.append(f"{label}.receipt_sha256 does not match canonical receipt content")
        previous_hash = declared_hash if isinstance(declared_hash, str) else None
    return index


def build_gate_receipt(
    state: dict[str, Any],
    gate: str,
    packet_id: str | None,
    unit_id: str | None,
    state_snapshot_ref: str,
) -> dict[str, Any]:
    receipts = state.get("gate_receipts", [])
    previous_hash = receipts[-1].get("receipt_sha256") if receipts else None
    receipt: dict[str, Any] = {
        "sequence": len(receipts) + 1,
        "gate": gate,
        "packet_id": packet_id,
        "unit_id": unit_id,
        "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "validated_state_sha256": compute_state_hash(state),
        "state_snapshot_ref": state_snapshot_ref,
        "previous_receipt_sha256": previous_hash,
    }
    receipt["receipt_sha256"] = compute_receipt_hash(receipt)
    return receipt


def validate_identity(
    record: dict[str, Any],
    label: str,
    producer: str,
    errors: list[str],
    *,
    execution_key: str = "execution_id",
) -> None:
    if record.get("producer_skill") != producer:
        errors.append(f"{label}.producer_skill must be {producer}")
    if not nonempty_string(record.get(execution_key)):
        errors.append(f"{label}.{execution_key} must be a non-empty string")


def validate_state(
    state: dict[str, Any], snapshot_root: Path | None = None
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    summary: dict[str, Any] = {}

    if state.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    for key in ("project_id", "run_id"):
        if not nonempty_string(state.get(key)):
            errors.append(f"{key} must be a non-empty string")
    mode = state.get("mode")
    if mode not in MODES:
        errors.append("mode must be new_publication or existing_publication_revision")
    if state.get("status") not in RUN_STATUSES:
        errors.append("status is not a supported large-publication run status")

    map_record = state.get("map")
    map_frozen_at: datetime | None = None
    map_revision: Any = None
    map_sha: Any = None
    if not isinstance(map_record, dict):
        errors.append("map must be an object")
        map_record = {}
    if not nonempty_string(map_record.get("artifact_id")):
        errors.append("map.artifact_id must be a non-empty string")
    map_revision = map_record.get("revision")
    if not isinstance(map_revision, int) or isinstance(map_revision, bool) or map_revision < 1:
        errors.append("map.revision must be a positive integer")
    map_sha = map_record.get("sha256")
    require_sha(map_sha, "map.sha256", errors)
    map_frozen_at = parse_time(map_record.get("frozen_at"), "map.frozen_at", errors)
    input_types = map_record.get("input_artifact_types")
    if not unique_string_list(input_types) or not input_types:
        errors.append("map.input_artifact_types must be a non-empty unique string list")
        input_types = []
    derived = map_record.get("derived_from_reader_draft")
    if not isinstance(derived, bool):
        errors.append("map.derived_from_reader_draft must be boolean")
    if mode == "new_publication":
        if derived is not False:
            errors.append("a new-publication map cannot be derived from reader-facing draft text")
        for artifact_type in input_types:
            if normalized_artifact_type(artifact_type) in FORBIDDEN_NEW_MAP_INPUT_TYPES:
                errors.append(
                    "a new-publication map cannot depend on generated draft, publication, "
                    f"checkpoint, claim, or Notion artifacts: {artifact_type}"
                )

    obligation_ids = state.get("obligation_ids")
    if not unique_string_list(obligation_ids) or not obligation_ids:
        errors.append("obligation_ids must be a non-empty unique string list")
        obligation_ids = []
    obligation_set = set(obligation_ids)

    packets = state.get("packets")
    if not isinstance(packets, list) or not all(isinstance(item, dict) for item in packets):
        errors.append("packets must be an object list")
        packets = []
    packet_ids = [packet.get("packet_id") for packet in packets]
    if any(not nonempty_string(item) for item in packet_ids) or len(packet_ids) != len(set(packet_ids)):
        errors.append("packet_id values must be unique and non-empty")
    packets_by_id = {
        packet["packet_id"]: packet
        for packet in packets
        if nonempty_string(packet.get("packet_id"))
    }
    ordinals = [packet.get("ordinal") for packet in packets]
    if any(not isinstance(item, int) or isinstance(item, bool) or item < 1 for item in ordinals):
        errors.append("packet ordinals must be positive integers")
    elif len(ordinals) != len(set(ordinals)):
        errors.append("packet ordinals must be unique")

    packet_times: dict[str, dict[str, datetime | None]] = {}
    author_execution_ids: dict[str, str] = {}
    dispatch_ids: dict[str, str] = {}
    scheduled_obligations: set[str] = set()
    dependencies: dict[str, list[str]] = {}

    for packet in packets:
        packet_id = packet.get("packet_id")
        label = f"packet {packet_id or '<unknown>'}"
        if not nonempty_string(packet_id):
            continue
        status = packet.get("status")
        if status not in PACKET_STATUSES:
            errors.append(f"{label} has an unsupported status")
        local_obligations = packet.get("obligation_ids")
        if not unique_string_list(local_obligations) or not local_obligations:
            errors.append(f"{label}.obligation_ids must be a non-empty unique string list")
            local_obligations = []
        unknown_obligations = sorted(set(local_obligations) - obligation_set)
        if unknown_obligations:
            errors.append(f"{label} contains unknown obligations: {', '.join(unknown_obligations)}")
        scheduled_obligations.update(local_obligations)
        dependency_ids = packet.get("depends_on")
        if not unique_string_list(dependency_ids):
            errors.append(f"{label}.depends_on must be a unique string list")
            dependency_ids = []
        if packet_id in dependency_ids:
            errors.append(f"{label} cannot depend on itself")
        dependencies[packet_id] = dependency_ids
        unknown_dependencies = sorted(set(dependency_ids) - set(packets_by_id))
        if unknown_dependencies:
            errors.append(f"{label} has unknown dependencies: {', '.join(unknown_dependencies)}")
        if packet.get("map_revision") != map_revision:
            errors.append(f"{label}.map_revision does not match the frozen map")
        if packet.get("map_sha256") != map_sha:
            errors.append(f"{label}.map_sha256 does not match the frozen map")
        if packet.get("scope_basis") not in SCOPE_BASES:
            errors.append(
                f"{label}.scope_basis must be obligation_cluster, argument_stage, "
                "context_split, or continuation"
            )

        capacity = packet.get("capacity")
        if not isinstance(capacity, dict):
            errors.append(f"{label}.capacity must be an object")
        else:
            capacity_keys = (
                "context_budget_tokens",
                "input_tokens_estimate",
                "output_tokens_reservation",
                "safety_margin_tokens",
            )
            values: dict[str, int] = {}
            for key in capacity_keys:
                value = capacity.get(key)
                if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                    errors.append(f"{label}.capacity.{key} must be a non-negative integer")
                else:
                    values[key] = value
            if values.get("context_budget_tokens", 0) == 0:
                errors.append(f"{label}.capacity.context_budget_tokens must be positive")
            if values.get("output_tokens_reservation", 0) == 0:
                errors.append(f"{label}.capacity.output_tokens_reservation must be positive")
            if len(values) == len(capacity_keys):
                required = (
                    values["input_tokens_estimate"]
                    + values["output_tokens_reservation"]
                    + values["safety_margin_tokens"]
                )
                if required > values["context_budget_tokens"]:
                    errors.append(f"{label}.capacity exceeds its context budget")

        dispatch = packet.get("dispatch")
        draft = packet.get("draft")
        checkpoint = packet.get("checkpoint")
        accepted_at_value = packet.get("accepted_at")
        dispatched_at = completed_at = checkpointed_at = accepted_at = None

        if status == "queued":
            if any(value is not None for value in (dispatch, draft, checkpoint, accepted_at_value)):
                errors.append(f"{label} is queued but already contains downstream state")
        if status in {"dispatched", "checkpointed", "accepted"}:
            if not isinstance(dispatch, dict):
                errors.append(f"{label}.dispatch must exist after dispatch")
            else:
                validate_identity(
                    dispatch,
                    f"{label}.dispatch",
                    "knowledge-product-orchestrator",
                    errors,
                    execution_key="dispatch_id",
                )
                dispatch_id = dispatch.get("dispatch_id")
                if nonempty_string(dispatch_id):
                    if dispatch_id in dispatch_ids.values():
                        errors.append(f"{label}.dispatch_id must identify one Packet only")
                    dispatch_ids[packet_id] = dispatch_id
                dispatched_at = parse_time(
                    dispatch.get("dispatched_at"), f"{label}.dispatch.dispatched_at", errors
                )
                if map_frozen_at and dispatched_at and dispatched_at < map_frozen_at:
                    errors.append(f"{label} was dispatched before the map was frozen")
            if status == "dispatched" and any(
                value is not None for value in (draft, checkpoint, accepted_at_value)
            ):
                errors.append(f"{label} is dispatched but contains uncheckpointed completion state")
        if status in {"checkpointed", "accepted"}:
            if not isinstance(draft, dict):
                errors.append(f"{label}.draft must exist after authoring")
            else:
                validate_identity(draft, f"{label}.draft", "notion-node-author", errors)
                execution_id = draft.get("execution_id")
                if nonempty_string(execution_id):
                    if execution_id in author_execution_ids.values():
                        errors.append(
                            f"{label}.draft.execution_id must identify one Packet invocation only"
                        )
                    author_execution_ids[packet_id] = execution_id
                if not nonempty_string(draft.get("content_ref")):
                    errors.append(f"{label}.draft.content_ref must be a non-empty string")
                require_sha(draft.get("content_sha256"), f"{label}.draft.content_sha256", errors)
                completed_at = parse_time(
                    draft.get("completed_at"), f"{label}.draft.completed_at", errors
                )
                if dispatched_at and completed_at and completed_at < dispatched_at:
                    errors.append(f"{label} draft completed before dispatch")
            if not isinstance(checkpoint, dict):
                errors.append(f"{label}.checkpoint must exist after authoring")
            else:
                if not nonempty_string(checkpoint.get("artifact_id")):
                    errors.append(f"{label}.checkpoint.artifact_id must be a non-empty string")
                require_sha(
                    checkpoint.get("checkpoint_sha256"),
                    f"{label}.checkpoint.checkpoint_sha256",
                    errors,
                )
                if isinstance(draft, dict) and checkpoint.get("content_sha256") != draft.get(
                    "content_sha256"
                ):
                    errors.append(f"{label} checkpoint is not bound to the authored draft hash")
                checkpointed_at = parse_time(
                    checkpoint.get("persisted_at"), f"{label}.checkpoint.persisted_at", errors
                )
                if completed_at and checkpointed_at and checkpointed_at < completed_at:
                    errors.append(f"{label} checkpoint predates draft completion")
            if status == "checkpointed" and accepted_at_value is not None:
                errors.append(f"{label} is checkpointed but already has accepted_at")
        if status == "accepted":
            accepted_at = parse_time(accepted_at_value, f"{label}.accepted_at", errors)
            if checkpointed_at and accepted_at and accepted_at < checkpointed_at:
                errors.append(f"{label} was accepted before checkpoint persistence")
        packet_times[packet_id] = {
            "dispatched": dispatched_at,
            "completed": completed_at,
            "checkpointed": checkpointed_at,
            "accepted": accepted_at,
        }

    # Reject dependency cycles even before any Packet is dispatched.
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(packet_id: str) -> None:
        if packet_id in visited:
            return
        if packet_id in visiting:
            errors.append(f"Packet dependency cycle includes {packet_id}")
            return
        visiting.add(packet_id)
        for dependency_id in dependencies.get(packet_id, []):
            if dependency_id in packets_by_id:
                visit(dependency_id)
        visiting.remove(packet_id)
        visited.add(packet_id)

    for packet_id in packets_by_id:
        visit(packet_id)

    for packet_id, dependency_ids in dependencies.items():
        dispatched_at = packet_times.get(packet_id, {}).get("dispatched")
        if not dispatched_at:
            continue
        for dependency_id in dependency_ids:
            dependency = packets_by_id.get(dependency_id)
            dependency_accepted = packet_times.get(dependency_id, {}).get("accepted")
            if dependency is not None and dependency.get("status") != "accepted":
                errors.append(f"packet {packet_id} was dispatched before {dependency_id} was accepted")
            elif dependency_accepted and dispatched_at < dependency_accepted:
                errors.append(f"packet {packet_id} dispatch predates {dependency_id} acceptance")

    units = state.get("units")
    if not isinstance(units, list) or not all(isinstance(item, dict) for item in units):
        errors.append("units must be an object list")
        units = []
    unit_ids = [unit.get("unit_id") for unit in units]
    if any(not nonempty_string(item) for item in unit_ids) or len(unit_ids) != len(set(unit_ids)):
        errors.append("unit_id values must be unique and non-empty")
    units_by_id = {
        unit["unit_id"]: unit for unit in units if nonempty_string(unit.get("unit_id"))
    }
    unit_packet_ids: list[str] = []
    publication_times: list[datetime] = []
    review_execution_ids: dict[str, str] = {}
    audit_execution_ids: dict[str, str] = {}
    publication_operation_ids: dict[str, str] = {}
    unit_times: dict[str, dict[str, datetime | None]] = {}
    minimum_run_phase = 0
    if any(
        packet.get("status") in {"dispatched", "checkpointed", "accepted"}
        for packet in packets
    ):
        minimum_run_phase = 1

    for unit in units:
        unit_id = unit.get("unit_id")
        label = f"unit {unit_id or '<unknown>'}"
        if not nonempty_string(unit_id):
            continue
        status = unit.get("status")
        if status not in UNIT_STATUSES:
            errors.append(f"{label} has an unsupported status")
        packet_refs = unit.get("packet_ids")
        if not unique_string_list(packet_refs) or not packet_refs:
            errors.append(f"{label}.packet_ids must be a non-empty unique string list")
            packet_refs = []
        unit_packet_ids.extend(packet_refs)
        unknown_packets = sorted(set(packet_refs) - set(packets_by_id))
        if unknown_packets:
            errors.append(f"{label} contains unknown Packets: {', '.join(unknown_packets)}")
        unit_obligations = {
            obligation
            for packet_id in packet_refs
            for obligation in packets_by_id.get(packet_id, {}).get("obligation_ids", [])
            if nonempty_string(obligation)
        }

        assembled_at: datetime | None = None
        assembled_sha = unit.get("assembled_draft_sha256")
        if status == "planned":
            forbidden = (
                "assembled_draft_ref",
                "assembled_draft_sha256",
                "assembled_at",
                "review",
                "repair",
                "finding_dispositions",
                "final_draft_sha256",
                "claim_audit",
                "publication",
            )
            if any(unit.get(key) is not None for key in forbidden):
                errors.append(f"{label} is planned but already contains downstream state")
        if status in {"assembled", "reviewed", "resolved", "audited", "published"}:
            minimum_run_phase = max(minimum_run_phase, 2)
            for packet_id in packet_refs:
                if packets_by_id.get(packet_id, {}).get("status") != "accepted":
                    errors.append(f"{label} uses Packet {packet_id} before it is accepted")
            if not nonempty_string(unit.get("assembled_draft_ref")):
                errors.append(f"{label}.assembled_draft_ref must be a non-empty string")
            require_sha(assembled_sha, f"{label}.assembled_draft_sha256", errors)
            assembled_at = parse_time(unit.get("assembled_at"), f"{label}.assembled_at", errors)
            for packet_id in packet_refs:
                accepted_at = packet_times.get(packet_id, {}).get("accepted")
                if assembled_at and accepted_at and assembled_at < accepted_at:
                    errors.append(f"{label} was assembled before Packet {packet_id} acceptance")

        review = unit.get("review")
        review_time: datetime | None = None
        findings: list[dict[str, Any]] = []
        if status == "assembled" and review is not None:
            errors.append(f"{label} is assembled but already contains review state")
        if status in {"reviewed", "resolved", "audited", "published"}:
            if not isinstance(review, dict):
                errors.append(f"{label}.review must exist after semantic review")
                review = {}
            validate_identity(review, f"{label}.review", "large-publication-architect", errors)
            if review.get("review_mode") != "model_semantic_review":
                errors.append(f"{label}.review.review_mode must be model_semantic_review")
            if review.get("basis") != "semantic_obligations_and_relationships":
                errors.append(
                    f"{label}.review.basis must be semantic_obligations_and_relationships"
                )
            if review.get("draft_sha256") != assembled_sha:
                errors.append(f"{label} review is not bound to the assembled draft hash")
            review_time = parse_time(review.get("reviewed_at"), f"{label}.review.reviewed_at", errors)
            if assembled_at and review_time and review_time < assembled_at:
                errors.append(f"{label} was reviewed before assembly")
            reviewed_obligations = review.get("obligation_ids")
            if not unique_string_list(reviewed_obligations):
                errors.append(f"{label}.review.obligation_ids must be a unique string list")
            elif set(reviewed_obligations) != unit_obligations:
                errors.append(f"{label} review does not cover the exact Packet obligation set")
            if not unique_string_list(review.get("relation_ids")):
                errors.append(f"{label}.review.relation_ids must be a unique string list")
            raw_findings = review.get("findings")
            if not isinstance(raw_findings, list) or not all(
                isinstance(item, dict) for item in raw_findings
            ):
                errors.append(f"{label}.review.findings must be an object list")
            else:
                findings = raw_findings
            finding_ids = [finding.get("finding_id") for finding in findings]
            if any(not nonempty_string(item) for item in finding_ids) or len(finding_ids) != len(
                set(finding_ids)
            ):
                errors.append(f"{label} review finding IDs must be unique and non-empty")
            for finding in findings:
                finding_id = finding.get("finding_id", "<unknown>")
                if finding.get("category") not in FINDING_CATEGORIES:
                    errors.append(f"{label} finding {finding_id} has an unsupported category")
                if not nonempty_string(finding.get("observation")):
                    errors.append(f"{label} finding {finding_id} needs a concrete observation")
                if not nonempty_string(finding.get("smallest_repair")):
                    errors.append(f"{label} finding {finding_id} needs the smallest repair")
            review_execution = review.get("execution_id")
            if nonempty_string(review_execution):
                if review_execution in review_execution_ids.values():
                    errors.append(f"{label} review execution ID must identify one review only")
                review_execution_ids[unit_id] = review_execution
            for packet_id in packet_refs:
                if review_execution == author_execution_ids.get(packet_id):
                    errors.append(f"{label} Architect review reused an Author execution ID")

        dispositions = unit.get("finding_dispositions")
        repair = unit.get("repair")
        final_sha = unit.get("final_draft_sha256")
        repair_time: datetime | None = None
        resolution_time: datetime | None = None
        if status == "reviewed" and findings and any(
            unit.get(key) is not None
            for key in (
                "repair",
                "finding_dispositions",
                "final_draft_sha256",
                "claim_audit",
                "publication",
            )
        ):
            errors.append(f"{label} has open findings but already contains downstream state")
        if status == "resolved" and not findings:
            errors.append(f"{label} cannot be resolved when the review has no findings")
        terminal_state = status in {"resolved", "audited", "published"} or (
            status == "reviewed" and not findings
        )
        if terminal_state:
            if not isinstance(dispositions, list) or not all(
                isinstance(item, dict) for item in dispositions
            ):
                errors.append(f"{label}.finding_dispositions must be an object list")
                dispositions = []
            disposition_ids = [item.get("finding_id") for item in dispositions]
            finding_ids = [item.get("finding_id") for item in findings]
            if set(disposition_ids) != set(finding_ids) or len(disposition_ids) != len(
                set(disposition_ids)
            ):
                errors.append(f"{label} dispositions must cover each review finding exactly once")
            repaired_finding = False
            disposition_times: dict[str, datetime | None] = {}
            for disposition in dispositions:
                finding_id = disposition.get("finding_id", "<unknown>")
                if disposition.get("disposition") not in DISPOSITIONS:
                    errors.append(f"{label} finding {finding_id} has an unsupported disposition")
                repaired_finding = repaired_finding or disposition.get("disposition") == "repaired"
                resolved_at = parse_time(
                    disposition.get("resolved_at"),
                    f"{label} finding {finding_id}.resolved_at",
                    errors,
                )
                disposition_times[finding_id] = resolved_at
                if review_time and resolved_at and resolved_at < review_time:
                    errors.append(f"{label} finding {finding_id} was resolved before review")
            resolved_times = [value for value in disposition_times.values() if value is not None]
            if resolved_times:
                resolution_time = max(resolved_times)
            if repaired_finding:
                if not isinstance(repair, dict):
                    errors.append(f"{label} repaired findings require one Author repair record")
                else:
                    validate_identity(repair, f"{label}.repair", "notion-node-author", errors)
                    if repair.get("input_draft_sha256") != assembled_sha:
                        errors.append(f"{label} repair input does not match the reviewed draft")
                    require_sha(
                        repair.get("output_draft_sha256"),
                        f"{label}.repair.output_draft_sha256",
                        errors,
                    )
                    repair_time = parse_time(
                        repair.get("repaired_at"), f"{label}.repair.repaired_at", errors
                    )
                    if review_time and repair_time and repair_time < review_time:
                        errors.append(f"{label} repair predates its review")
                    repair_execution = repair.get("execution_id")
                    if repair_execution == review.get("execution_id"):
                        errors.append(f"{label} repair reused the Architect execution ID")
                    if repair_execution in {
                        author_execution_ids.get(packet_id) for packet_id in packet_refs
                    }:
                        errors.append(f"{label} repair must be a distinct bounded Author execution")
                    if final_sha != repair.get("output_draft_sha256"):
                        errors.append(f"{label} final draft hash does not match the repair output")
                    for disposition in dispositions:
                        if disposition.get("disposition") != "repaired":
                            continue
                        finding_id = disposition.get("finding_id", "<unknown>")
                        resolved_at = disposition_times.get(finding_id)
                        if repair_time and resolved_at and resolved_at < repair_time:
                            errors.append(
                                f"{label} repaired finding {finding_id} was resolved before repair"
                            )
            else:
                if repair is not None:
                    errors.append(f"{label} has a repair without a repaired finding")
                if final_sha != assembled_sha:
                    errors.append(f"{label} final draft hash must equal the reviewed draft")
            require_sha(final_sha, f"{label}.final_draft_sha256", errors)

        claim_audit = unit.get("claim_audit")
        audit_time: datetime | None = None
        if status in {"audited", "published"}:
            minimum_run_phase = max(minimum_run_phase, 3)
            if not isinstance(claim_audit, dict):
                errors.append(f"{label}.claim_audit must exist after claim audit")
                claim_audit = {}
            validate_identity(claim_audit, f"{label}.claim_audit", "zotero-source-gate", errors)
            if claim_audit.get("status") not in PASSING_AUDITS:
                errors.append(f"{label}.claim_audit is not passing")
            if not nonempty_string(claim_audit.get("receipt_ref")):
                errors.append(f"{label}.claim_audit.receipt_ref must be a non-empty string")
            if claim_audit.get("audited_draft_sha256") != final_sha:
                errors.append(f"{label} claim audit is not bound to the final draft hash")
            audit_time = parse_time(
                claim_audit.get("audited_at"), f"{label}.claim_audit.audited_at", errors
            )
            audit_execution = claim_audit.get("execution_id")
            if nonempty_string(audit_execution):
                if audit_execution in audit_execution_ids.values():
                    errors.append(f"{label} audit execution ID must identify one audit only")
                audit_execution_ids[unit_id] = audit_execution
            previous_time = repair_time or review_time
            if previous_time and audit_time and audit_time < previous_time:
                errors.append(f"{label} claim audit predates review resolution")

        citation_projection = unit.get("citation_projection")
        projection_time: datetime | None = None
        projected_sha: str | None = None
        if citation_projection is not None:
            if not isinstance(citation_projection, dict):
                errors.append(f"{label}.citation_projection must be an object")
                citation_projection = {}
            validate_identity(
                citation_projection,
                f"{label}.citation_projection",
                "notion-node-author",
                errors,
            )
            if citation_projection.get("status") != "passed":
                errors.append(f"{label}.citation_projection.status must be passed")
            if not nonempty_string(citation_projection.get("manifest_ref")):
                errors.append(
                    f"{label}.citation_projection.manifest_ref must be a non-empty string"
                )
            if not nonempty_string(citation_projection.get("validation_receipt_ref")):
                errors.append(
                    f"{label}.citation_projection.validation_receipt_ref must be a non-empty string"
                )
            if citation_projection.get("source_draft_sha256") != final_sha:
                errors.append(
                    f"{label} citation projection is not bound to the audited fact draft"
                )
            projected_sha = citation_projection.get("projected_draft_sha256")
            require_sha(
                projected_sha,
                f"{label}.citation_projection.projected_draft_sha256",
                errors,
            )
            projection_time = parse_time(
                citation_projection.get("projected_at"),
                f"{label}.citation_projection.projected_at",
                errors,
            )
            if audit_time and projection_time and projection_time < audit_time:
                errors.append(f"{label} citation projection predates claim audit")

        publication = unit.get("publication")
        if status == "published":
            minimum_run_phase = max(minimum_run_phase, 4)
            if not isinstance(citation_projection, dict):
                errors.append(f"{label}.citation_projection must exist before publication")
            if not isinstance(publication, dict):
                errors.append(f"{label}.publication must exist after publication")
                publication = {}
            validate_identity(
                publication,
                f"{label}.publication",
                "notion-node-author",
                errors,
                execution_key="operation_id",
            )
            if publication.get("status") != "succeeded":
                errors.append(f"{label}.publication.status must be succeeded")
            if not nonempty_string(publication.get("target_id")):
                errors.append(f"{label}.publication.target_id must be a non-empty string")
            if publication.get("published_draft_sha256") != projected_sha:
                errors.append(f"{label} publication is not bound to the projected draft")
            published_at = parse_time(
                publication.get("published_at"), f"{label}.publication.published_at", errors
            )
            operation_id = publication.get("operation_id")
            if nonempty_string(operation_id):
                if operation_id in publication_operation_ids.values():
                    errors.append(f"{label} publication operation ID must be unique")
                publication_operation_ids[unit_id] = operation_id
            if projection_time and published_at and published_at < projection_time:
                errors.append(f"{label} was published before citation projection")
            if published_at:
                publication_times.append(published_at)

        unit_times[unit_id] = {
            "assembled": assembled_at,
            "reviewed": review_time,
            "repaired": repair_time,
            "resolved": resolution_time,
            "audited": audit_time,
            "projected": projection_time,
            "published": published_at if status == "published" else None,
        }

    receipt_index = validate_gate_receipts(state, errors, snapshot_root)
    completion = state.get("completion")
    if not isinstance(completion, dict):
        errors.append("completion must be an object")
        completion = {}
    completion_status = completion.get("status")
    if completion_status not in {"pending", "complete"}:
        errors.append("completion.status must be pending or complete")
    if completion_status == "pending" and completion.get("declared_at") is not None:
        errors.append("pending completion must not have declared_at")
    if completion_status == "complete":
        declared_at = parse_time(completion.get("declared_at"), "completion.declared_at", errors)
        if state.get("status") != "complete":
            errors.append("run status must be complete when completion is complete")
        incomplete_packets = [
            packet_id
            for packet_id, packet in packets_by_id.items()
            if packet.get("status") != "accepted"
        ]
        if incomplete_packets:
            errors.append("completion has non-accepted Packets: " + ", ".join(incomplete_packets))
        unscheduled = sorted(obligation_set - scheduled_obligations)
        if unscheduled:
            errors.append("completion has unscheduled obligations: " + ", ".join(unscheduled))
        if len(unit_packet_ids) != len(set(unit_packet_ids)):
            errors.append("completion assigns a Packet to more than one coherent unit")
        uncovered_packets = sorted(set(packets_by_id) - set(unit_packet_ids))
        if uncovered_packets:
            errors.append("completion has Packets outside coherent units: " + ", ".join(uncovered_packets))
        unpublished_units = [
            unit_id for unit_id, unit in units_by_id.items() if unit.get("status") != "published"
        ]
        if unpublished_units:
            errors.append("completion has unpublished units: " + ", ".join(unpublished_units))
        required_receipts: set[tuple[str, str | None]] = {("map-ready", None)}
        for packet_id in packets_by_id:
            required_receipts.add(("packet-dispatch", packet_id))
            required_receipts.add(("packet-checkpoint", packet_id))
        for unit_id in units_by_id:
            required_receipts.add(("review-ready", unit_id))
            required_receipts.add(("review-recorded", unit_id))
            required_receipts.add(("claim-audit-ready", unit_id))
            required_receipts.add(("publish-ready", unit_id))
        missing_receipts = sorted(
            required_receipts - set(receipt_index), key=lambda item: (item[0], item[1] or "")
        )
        if missing_receipts:
            errors.append(
                "completion is missing prospective gate receipts: "
                + ", ".join(
                    f"{gate}:{subject}" if subject else gate
                    for gate, subject in missing_receipts
                )
            )
        map_receipt_time = receipt_index.get(("map-ready", None))
        dispatch_times = [
            times.get("dispatched")
            for times in packet_times.values()
            if times.get("dispatched") is not None
        ]
        if map_receipt_time and dispatch_times and map_receipt_time > min(dispatch_times):
            errors.append("map-ready receipt postdates the first Packet dispatch")
        for packet_id, times in packet_times.items():
            dispatch_receipt = receipt_index.get(("packet-dispatch", packet_id))
            checkpoint_receipt = receipt_index.get(("packet-checkpoint", packet_id))
            if dispatch_receipt and times.get("dispatched") and dispatch_receipt > times["dispatched"]:
                errors.append(f"packet {packet_id} dispatch receipt postdates dispatch")
            if checkpoint_receipt and times.get("checkpointed") and checkpoint_receipt < times[
                "checkpointed"
            ]:
                errors.append(f"packet {packet_id} checkpoint receipt predates persistence")
            if checkpoint_receipt and times.get("accepted") and checkpoint_receipt > times["accepted"]:
                errors.append(f"packet {packet_id} checkpoint receipt postdates acceptance")
        for unit_id, times in unit_times.items():
            review_ready = receipt_index.get(("review-ready", unit_id))
            review_recorded = receipt_index.get(("review-recorded", unit_id))
            claim_ready = receipt_index.get(("claim-audit-ready", unit_id))
            publish_ready = receipt_index.get(("publish-ready", unit_id))
            review_resolution = times.get("resolved") or times.get("repaired") or times.get(
                "reviewed"
            )
            review_recorded_limit = times.get("repaired") or times.get("resolved") or times.get(
                "audited"
            )
            if review_ready and times.get("assembled") and review_ready < times["assembled"]:
                errors.append(f"unit {unit_id} review-ready receipt predates assembly")
            if review_ready and times.get("reviewed") and review_ready > times["reviewed"]:
                errors.append(f"unit {unit_id} review-ready receipt postdates review")
            if review_recorded and times.get("reviewed") and review_recorded < times["reviewed"]:
                errors.append(f"unit {unit_id} review-recorded receipt predates review")
            if review_recorded and review_recorded_limit and review_recorded > review_recorded_limit:
                errors.append(f"unit {unit_id} review-recorded receipt postdates resolution")
            if claim_ready and review_resolution and claim_ready < review_resolution:
                errors.append(f"unit {unit_id} claim-audit-ready receipt predates review resolution")
            if claim_ready and times.get("audited") and claim_ready > times["audited"]:
                errors.append(f"unit {unit_id} claim-audit-ready receipt postdates audit")
            if publish_ready and times.get("audited") and publish_ready < times["audited"]:
                errors.append(f"unit {unit_id} publish-ready receipt predates audit")
            if publish_ready and times.get("projected") and publish_ready < times["projected"]:
                errors.append(f"unit {unit_id} publish-ready receipt predates citation projection")
            if publish_ready and times.get("published") and publish_ready > times["published"]:
                errors.append(f"unit {unit_id} publish-ready receipt postdates publication")
        if declared_at and publication_times and declared_at < max(publication_times):
            errors.append("completion was declared before the final publication result")
    elif state.get("status") == "complete":
        errors.append("run status cannot be complete while completion is pending")

    run_phase = {
        "mapped": 0,
        "authoring": 1,
        "reviewing": 2,
        "auditing": 3,
        "publishing": 4,
        "complete": 5,
    }.get(state.get("status"))
    if run_phase is not None and run_phase < minimum_run_phase:
        errors.append("run status is behind its most advanced Packet or unit state")
    has_stale_state = any(packet.get("status") == "stale" for packet in packets) or any(
        unit.get("status") == "stale" for unit in units
    )
    if has_stale_state and state.get("status") != "invalidated":
        errors.append("stale Packet or unit state requires run status invalidated")
    if state.get("status") == "invalidated" and completion_status == "complete":
        errors.append("an invalidated run cannot declare completion")

    summary.update(
        {
            "obligation_count": len(obligation_set),
            "packet_count": len(packets_by_id),
            "scheduled_obligation_count": len(scheduled_obligations),
            "unit_count": len(units_by_id),
            "completion_status": completion_status,
        }
    )
    return errors, summary


def validate_gate(
    state: dict[str, Any], gate: str, packet_id: str | None, unit_id: str | None
) -> list[str]:
    errors: list[str] = []
    packets = state.get("packets") if isinstance(state.get("packets"), list) else []
    units = state.get("units") if isinstance(state.get("units"), list) else []
    packets_by_id = {
        packet.get("packet_id"): packet
        for packet in packets
        if isinstance(packet, dict) and nonempty_string(packet.get("packet_id"))
    }
    units_by_id = {
        unit.get("unit_id"): unit
        for unit in units
        if isinstance(unit, dict) and nonempty_string(unit.get("unit_id"))
    }

    if gate == "map-ready":
        if any(packet.get("status") != "queued" for packet in packets_by_id.values()):
            errors.append("map-ready requires every Packet to remain queued")
        if any(unit.get("status") != "planned" for unit in units_by_id.values()):
            errors.append("map-ready requires every coherent unit to remain planned")
        if state.get("completion", {}).get("status") != "pending":
            errors.append("map-ready requires pending completion")
        return errors

    if gate in {"packet-dispatch", "packet-checkpoint"}:
        if not packet_id:
            return [f"{gate} requires --packet-id"]
        packet = packets_by_id.get(packet_id)
        if packet is None:
            return [f"unknown Packet {packet_id}"]
        if gate == "packet-dispatch":
            if packet.get("status") != "queued":
                errors.append("packet-dispatch requires a queued Packet")
            for dependency_id in packet.get("depends_on", []):
                if packets_by_id.get(dependency_id, {}).get("status") != "accepted":
                    errors.append(
                        f"packet-dispatch requires dependency {dependency_id} to be accepted"
                    )
        else:
            if packet.get("status") != "checkpointed":
                errors.append("packet-checkpoint is prospective and requires exact checkpointed state")
        return errors

    if gate in {
        "review-ready",
        "review-recorded",
        "claim-audit-ready",
        "publish-ready",
    }:
        if not unit_id:
            return [f"{gate} requires --unit-id"]
        unit = units_by_id.get(unit_id)
        if unit is None:
            return [f"unknown unit {unit_id}"]
        status = unit.get("status")
        if gate == "review-ready":
            if status != "assembled" or unit.get("review") is not None:
                errors.append("review-ready requires an assembled, not-yet-reviewed unit")
        elif gate == "review-recorded":
            if status != "reviewed":
                errors.append("review-recorded is prospective and requires exact reviewed state")
        elif gate == "claim-audit-ready":
            if status not in {"reviewed", "resolved"}:
                errors.append("claim-audit-ready requires reviewed and resolved semantic state")
            if unit.get("claim_audit") is not None:
                errors.append("claim-audit-ready requires claim audit to be absent")
            review = unit.get("review") if isinstance(unit.get("review"), dict) else {}
            findings = review.get("findings") if isinstance(review.get("findings"), list) else []
            if findings and status != "resolved":
                errors.append("claim-audit-ready requires resolved state when review has findings")
            if not findings and status != "reviewed":
                errors.append("claim-audit-ready requires reviewed state when review has no findings")
            dispositions = (
                unit.get("finding_dispositions")
                if isinstance(unit.get("finding_dispositions"), list)
                else []
            )
            if {item.get("finding_id") for item in findings if isinstance(item, dict)} != {
                item.get("finding_id") for item in dispositions if isinstance(item, dict)
            }:
                errors.append("claim-audit-ready requires every review finding to be resolved")
            if not isinstance(unit.get("final_draft_sha256"), str) or not SHA256.fullmatch(
                unit["final_draft_sha256"]
            ):
                errors.append("claim-audit-ready requires a final canonical draft hash")
        elif gate == "publish-ready":
            if status != "audited" or unit.get("publication") is not None:
                errors.append("publish-ready requires audited, not-yet-published state")
            projection = unit.get("citation_projection")
            if not isinstance(projection, dict) or projection.get("status") != "passed":
                errors.append("publish-ready requires a passing CitationProjection")
            elif projection.get("source_draft_sha256") != unit.get("final_draft_sha256"):
                errors.append("publish-ready requires CitationProjection for the audited fact draft")
            elif not isinstance(projection.get("projected_draft_sha256"), str) or not SHA256.fullmatch(
                projection["projected_draft_sha256"]
            ):
                errors.append("publish-ready requires a valid projected draft hash")
        return errors

    if gate == "complete":
        if state.get("completion", {}).get("status") != "complete":
            errors.append("complete gate requires a complete declaration")
        return errors
    return [f"unsupported gate {gate}"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path, help="JSON LargePublicationRunState")
    parser.add_argument("--gate", choices=sorted(GATES), help="prospective workflow gate")
    parser.add_argument("--packet-id", help="Packet selected for a Packet gate")
    parser.add_argument("--unit-id", help="coherent unit selected for a unit gate")
    parser.add_argument(
        "--snapshot-root",
        type=Path,
        help="root containing immutable pre-transition state snapshots",
    )
    args = parser.parse_args()
    try:
        state = load_state(args.state)
        snapshot_root = args.snapshot_root.resolve() if args.snapshot_root else None
        errors, summary = validate_state(state, snapshot_root)
        state_snapshot_ref: str | None = None
        if args.gate and snapshot_root is None:
            errors.append("workflow gates require --snapshot-root")
        elif args.gate and args.gate != "complete" and snapshot_root is not None:
            state_path = args.state.resolve()
            try:
                state_snapshot_ref = state_path.relative_to(snapshot_root).as_posix()
            except ValueError:
                errors.append("prospective gate state file must be inside --snapshot-root")
        if args.gate:
            errors.extend(validate_gate(state, args.gate, args.packet_id, args.unit_id))
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in dict.fromkeys(errors):
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    summary["gate"] = args.gate
    summary["packet_id"] = args.packet_id
    summary["state_sha256"] = compute_state_hash(state)
    summary["unit_id"] = args.unit_id
    summary["valid"] = True
    if args.gate and args.gate != "complete" and state_snapshot_ref is not None:
        summary["gate_receipt"] = build_gate_receipt(
            state,
            args.gate,
            args.packet_id,
            args.unit_id,
            state_snapshot_ref,
        )
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
