#!/usr/bin/env python3
"""Compute a DraftClaimSet hash and optionally validate its ClaimAuditReceipt."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any


PASSING_AUDIT_STATUSES = {"passed", "passed_with_caveat"}
PASSING_RESULTS = {"direct", "partial"}
SOURCE_IDENTITY_KEYS = {"source_id", "source_record_id", "zotero_item_key"}
STRUCTURED_SOURCE_IDENTITY_KEYS = SOURCE_IDENTITY_KEYS | {
    "doi",
    "isbn",
    "url",
    "commit_hash",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
LOCATOR_KINDS = {
    "page",
    "page_range",
    "section",
    "subsection",
    "paragraph",
    "timestamp",
    "time_range",
    "line_range",
    "table",
    "figure",
    "equation",
    "record",
}
EVIDENCE_CHECKSUM_KEYS = {
    "evidence_pack_checksum",
    "checksum",
    "sha256",
    "content_sha256",
}


def load_object(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: document root must be an object")
    return data


def unwrap(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key, data)
    if not isinstance(value, dict):
        raise ValueError(f"{key} must be an object")
    return value


def canonical_json(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        if not -(2**53 - 1) <= value <= 2**53 - 1:
            raise ValueError("integer is outside the JCS interoperable range")
        return str(value)
    if isinstance(value, float):
        raise ValueError("floating-point values are prohibited in DraftClaimSet hashing")
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, list):
        return "[" + ",".join(canonical_json(item) for item in value) + "]"
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise ValueError("all object keys must be strings")
        keys = sorted(value, key=lambda key: key.encode("utf-16-be"))
        return "{" + ",".join(
            canonical_json(key) + ":" + canonical_json(value[key]) for key in keys
        ) + "}"
    raise ValueError(f"unsupported JSON value type: {type(value).__name__}")


def compute_hash(draft: dict[str, Any]) -> str:
    if draft.get("canonicalization") != "jcs":
        raise ValueError("DraftClaimSet canonicalization must be jcs")
    payload = {key: value for key, value in draft.items() if key != "audited_draft_hash"}
    encoded = canonical_json(payload).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def evidence_unit_id(unit: dict[str, Any]) -> Any:
    for key in ("evidence_unit_id", "unit_id", "id"):
        if unit.get(key):
            return unit[key]
    return None


def locator_is_specific(locator: Any) -> bool:
    if not isinstance(locator, dict) or locator.get("kind") not in LOCATOR_KINDS:
        return False
    value = locator.get("value")
    if not (
        isinstance(value, (str, int))
        and not isinstance(value, bool)
        and bool(str(value).strip())
    ):
        return False
    if locator.get("kind") in {"section", "subsection"}:
        anchor = locator.get("anchor")
        return isinstance(anchor, str) and bool(anchor.strip())
    return True


def compute_evidence_pack_hash(evidence_pack: dict[str, Any]) -> str:
    payload = {
        key: value
        for key, value in evidence_pack.items()
        if key not in EVIDENCE_CHECKSUM_KEYS
    }
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def validate_evidence_pack(
    draft: dict[str, Any], evidence_pack: dict[str, Any]
) -> tuple[list[str], set[str], dict[str, set[str]]]:
    errors: list[str] = []
    if evidence_pack.get("canonicalization") != "jcs":
        errors.append("EvidencePack canonicalization must be jcs")
    pack_id = evidence_pack.get("evidence_pack_id", evidence_pack.get("artifact_id"))
    if not isinstance(pack_id, str) or not pack_id.strip():
        errors.append("EvidencePack must declare evidence_pack_id or artifact_id")
    elif draft.get("evidence_pack_id") != pack_id:
        errors.append("DraftClaimSet evidence_pack_id does not match EvidencePack")
    pack_checksum = next(
        (
            evidence_pack.get(key)
            for key in ("evidence_pack_checksum", "checksum", "sha256", "content_sha256")
            if isinstance(evidence_pack.get(key), str) and evidence_pack.get(key)
        ),
        None,
    )
    if pack_checksum is None or not SHA256.fullmatch(pack_checksum):
        errors.append("EvidencePack must declare an immutable lowercase SHA-256 checksum")
    else:
        computed_pack_checksum = compute_evidence_pack_hash(evidence_pack)
        if pack_checksum != computed_pack_checksum:
            errors.append("EvidencePack checksum does not match its canonical content")
        if draft.get("evidence_pack_checksum") != pack_checksum:
            errors.append("DraftClaimSet evidence_pack_checksum does not match EvidencePack")

    units = evidence_pack.get("evidence_units")
    if not isinstance(units, list) or not all(isinstance(item, dict) for item in units):
        errors.append("EvidencePack evidence_units must be an object list")
        units = []
    unit_ids = [evidence_unit_id(unit) for unit in units]
    if len(unit_ids) != len(set(unit_ids)) or any(
        not isinstance(unit_id, str) or not unit_id for unit_id in unit_ids
    ):
        errors.append("EvidencePack EvidenceUnit IDs must be unique and non-empty")
    valid_ids = {
        unit_id for unit_id in unit_ids if isinstance(unit_id, str) and unit_id
    }
    claim_ids = {
        claim.get("claim_id")
        for claim in draft.get("claims", [])
        if isinstance(claim, dict) and isinstance(claim.get("claim_id"), str)
    }
    supported_claims_by_unit: dict[str, set[str]] = {}
    for unit in units:
        unit_id = evidence_unit_id(unit) or "<unknown>"
        source_identity = unit.get("source_identity")
        has_source_identity = any(
            isinstance(unit.get(key), str) and bool(unit[key].strip())
            for key in SOURCE_IDENTITY_KEYS
        ) or (
            isinstance(source_identity, dict)
            and any(
                isinstance(source_identity.get(key), str)
                and bool(source_identity[key].strip())
                for key in STRUCTURED_SOURCE_IDENTITY_KEYS
            )
        )
        if not has_source_identity:
            errors.append(
                f"EvidenceUnit {unit_id} requires a concrete source or Zotero item identity"
            )
        if not locator_is_specific(unit.get("locator")):
            errors.append(
                f"EvidenceUnit {unit_id} requires a structured passage, table, figure, "
                "equation, timestamp, line, section, or record locator"
            )
        supported_claim_ids = unit.get("supported_claim_ids")
        if not isinstance(supported_claim_ids, list) or not all(
            isinstance(claim_id, str) and claim_id for claim_id in supported_claim_ids
        ) or not supported_claim_ids:
            errors.append(f"EvidenceUnit {unit_id} requires supported_claim_ids")
            supported_claim_ids = []
        elif len(supported_claim_ids) != len(set(supported_claim_ids)):
            errors.append(f"EvidenceUnit {unit_id} supported_claim_ids must be unique")
        unknown_claim_ids = sorted(set(supported_claim_ids) - claim_ids)
        if unknown_claim_ids:
            errors.append(
                f"EvidenceUnit {unit_id} references unknown claims: "
                + ", ".join(unknown_claim_ids)
            )
        if isinstance(unit_id, str):
            supported_claims_by_unit[unit_id] = set(supported_claim_ids)
        if not isinstance(unit.get("support_scope"), str) or not unit["support_scope"].strip():
            errors.append(f"EvidenceUnit {unit_id} requires a non-empty support_scope")
        if not isinstance(unit.get("content_fingerprint"), str) or not SHA256.fullmatch(
            unit["content_fingerprint"]
        ):
            errors.append(
                f"EvidenceUnit {unit_id} requires a lowercase SHA-256 content_fingerprint"
            )
        accessibility = unit.get("accessibility", unit.get("accessible"))
        if not (
            isinstance(accessibility, bool)
            or (isinstance(accessibility, str) and bool(accessibility.strip()))
        ):
            errors.append(f"EvidenceUnit {unit_id} requires accessibility state")
        if not isinstance(unit.get("conflict_status"), str) or not unit[
            "conflict_status"
        ].strip():
            errors.append(f"EvidenceUnit {unit_id} requires conflict_status")
    return errors, valid_ids, supported_claims_by_unit


def validate_receipt(
    draft: dict[str, Any],
    receipt: dict[str, Any],
    computed_hash: str,
    evidence_unit_ids: set[str] | None = None,
    supported_claims_by_unit: dict[str, set[str]] | None = None,
) -> list[str]:
    errors: list[str] = []
    declared_hash = draft.get("audited_draft_hash")
    if declared_hash != computed_hash:
        errors.append("DraftClaimSet audited_draft_hash does not match canonical content")
    if receipt.get("audited_draft_hash") != computed_hash:
        errors.append("ClaimAuditReceipt hash does not match the current DraftClaimSet")
    comparisons = (
        ("draft_claim_set_id", "draft_claim_set_id"),
        ("evidence_pack_id", "evidence_pack_id"),
        ("evidence_pack_checksum", "evidence_pack_checksum"),
        ("framework_revision", "framework_revision"),
        ("framework_diff_hash", "framework_diff_hash"),
    )
    for draft_key, receipt_key in comparisons:
        if draft.get(draft_key) != receipt.get(receipt_key):
            errors.append(f"ClaimAuditReceipt {receipt_key} does not match DraftClaimSet")
    draft_source_revisions = draft.get("source_revisions")
    receipt_source_revisions = receipt.get("source_revisions")
    if not isinstance(draft_source_revisions, dict):
        errors.append("DraftClaimSet source_revisions must be a mapping")
    if not isinstance(receipt_source_revisions, dict):
        errors.append("ClaimAuditReceipt source_revisions must be a mapping")
    if (
        isinstance(draft_source_revisions, dict)
        and isinstance(receipt_source_revisions, dict)
        and draft_source_revisions != receipt_source_revisions
    ):
        errors.append("ClaimAuditReceipt source_revisions do not match DraftClaimSet")
    audit_status = receipt.get("audit_status")
    if audit_status not in PASSING_AUDIT_STATUSES:
        errors.append("ClaimAuditReceipt is not passing")
    claims = draft.get("claims")
    results = receipt.get("claim_results")
    if not isinstance(claims, list) or not all(isinstance(item, dict) for item in claims):
        errors.append("DraftClaimSet claims must be an object list")
        claims = []
    if not isinstance(results, list) or not all(isinstance(item, dict) for item in results):
        errors.append("ClaimAuditReceipt claim_results must be an object list")
        results = []
    claim_ids = [item.get("claim_id") for item in claims]
    result_ids = [item.get("claim_id") for item in results]
    if len(claim_ids) != len(set(claim_ids)) or any(not item for item in claim_ids):
        errors.append("DraftClaimSet claim_id values must be unique and non-empty")
    if len(result_ids) != len(set(result_ids)) or any(not item for item in result_ids):
        errors.append("ClaimAuditReceipt claim_id values must be unique and non-empty")
    if set(claim_ids) != set(result_ids):
        errors.append("ClaimAuditReceipt does not cover the exact DraftClaimSet claim IDs")
    claims_by_id = {
        item.get("claim_id"): item
        for item in claims
        if isinstance(item.get("claim_id"), str) and item.get("claim_id")
    }
    results_by_id = {
        item.get("claim_id"): item
        for item in results
        if isinstance(item.get("claim_id"), str) and item.get("claim_id")
    }
    for claim_id in sorted(set(claims_by_id) & set(results_by_id)):
        claim_text = claims_by_id[claim_id].get("text", claims_by_id[claim_id].get("claim_text"))
        if not isinstance(claim_text, str) or not claim_text.strip():
            errors.append(f"DraftClaimSet claim {claim_id} requires exact claim text")
        target_section = claims_by_id[claim_id].get(
            "target_section", claims_by_id[claim_id].get("section")
        )
        if not isinstance(target_section, str) or not target_section.strip():
            errors.append(f"DraftClaimSet claim {claim_id} requires a target section")
        claim_evidence_ids = claims_by_id[claim_id].get("evidence_unit_ids")
        result_evidence_ids = results_by_id[claim_id].get("evidence_unit_ids")
        if not isinstance(claim_evidence_ids, list) or not all(
            isinstance(item, str) and item for item in claim_evidence_ids
        ):
            errors.append(f"DraftClaimSet claim {claim_id} evidence_unit_ids must be a string list")
        if not isinstance(result_evidence_ids, list) or not all(
            isinstance(item, str) and item for item in result_evidence_ids
        ):
            errors.append(
                f"ClaimAuditReceipt claim {claim_id} evidence_unit_ids must be a string list"
            )
        if (
            isinstance(claim_evidence_ids, list)
            and isinstance(result_evidence_ids, list)
            and claim_evidence_ids != result_evidence_ids
        ):
            errors.append(
                f"ClaimAuditReceipt claim {claim_id} evidence_unit_ids do not match DraftClaimSet"
            )
        if isinstance(claim_evidence_ids, list) and not claim_evidence_ids:
            errors.append(f"DraftClaimSet claim {claim_id} requires at least one EvidenceUnit")
        if evidence_unit_ids is not None and isinstance(claim_evidence_ids, list):
            unresolved_ids = sorted(set(claim_evidence_ids) - evidence_unit_ids)
            if unresolved_ids:
                errors.append(
                    f"DraftClaimSet claim {claim_id} references unknown EvidenceUnits: "
                    + ", ".join(unresolved_ids)
                )
            if supported_claims_by_unit is not None:
                mismatched_ids = sorted(
                    evidence_id
                    for evidence_id in claim_evidence_ids
                    if claim_id not in supported_claims_by_unit.get(evidence_id, set())
                )
                if mismatched_ids:
                    errors.append(
                        f"DraftClaimSet claim {claim_id} is outside EvidenceUnit support scope: "
                        + ", ".join(mismatched_ids)
                    )
        if evidence_unit_ids is not None:
            assessment = results_by_id[claim_id].get("support_assessment")
            if not isinstance(assessment, str) or not assessment.strip():
                errors.append(
                    f"ClaimAuditReceipt claim {claim_id} requires a support_assessment"
                )

        caveat_ids = results_by_id[claim_id].get("propagated_caveat_ids")
        if not isinstance(caveat_ids, list) or not all(
            isinstance(item, str) and item for item in caveat_ids
        ):
            errors.append(
                f"ClaimAuditReceipt claim {claim_id} propagated_caveat_ids must be a string list"
            )
            caveat_ids = []
        elif len(caveat_ids) != len(set(caveat_ids)):
            errors.append(
                f"ClaimAuditReceipt claim {claim_id} propagated_caveat_ids must be unique"
            )
        if results_by_id[claim_id].get("result") == "partial" and not caveat_ids:
            errors.append(
                f"ClaimAuditReceipt partial claim {claim_id} requires propagated caveat IDs"
            )
    result_values = [item.get("result") for item in results]
    if any(value not in PASSING_RESULTS for value in result_values):
        errors.append("ClaimAuditReceipt contains a contradictory or unsupported claim")
    if "partial" in result_values and audit_status != "passed_with_caveat":
        errors.append("a partial claim result requires passed_with_caveat")
    propagated_caveats = [
        caveat_id
        for item in results
        if isinstance(item.get("propagated_caveat_ids"), list)
        for caveat_id in item["propagated_caveat_ids"]
        if isinstance(caveat_id, str) and caveat_id
    ]
    if audit_status == "passed_with_caveat" and not propagated_caveats:
        errors.append("passed_with_caveat requires at least one propagated caveat ID")
    if audit_status == "passed" and propagated_caveats:
        errors.append("propagated caveats require passed_with_caveat")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="JSON DraftClaimSet document")
    parser.add_argument("--receipt", type=Path, help="JSON ClaimAuditReceipt document")
    parser.add_argument(
        "--evidence-pack",
        type=Path,
        help="JSON EvidencePack used to resolve exact EvidenceUnit identities and locators",
    )
    parser.add_argument(
        "--require-declared-hash",
        action="store_true",
        help="fail unless the draft declares the computed hash",
    )
    args = parser.parse_args()
    try:
        draft = unwrap(load_object(args.draft), "draft_claim_set")
        computed_hash = compute_hash(draft)
        errors: list[str] = []
        evidence_ids: set[str] | None = None
        supported_claims: dict[str, set[str]] | None = None
        if args.evidence_pack is not None:
            evidence_pack = unwrap(load_object(args.evidence_pack), "evidence_pack")
            evidence_errors, evidence_ids, supported_claims = validate_evidence_pack(
                draft, evidence_pack
            )
            errors.extend(evidence_errors)
        if args.require_declared_hash and draft.get("audited_draft_hash") != computed_hash:
            errors.append("DraftClaimSet audited_draft_hash does not match canonical content")
        if args.receipt is not None:
            receipt = unwrap(load_object(args.receipt), "claim_audit_receipt")
            errors.extend(
                validate_receipt(
                    draft,
                    receipt,
                    computed_hash,
                    evidence_ids,
                    supported_claims,
                )
            )
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in dict.fromkeys(errors):
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "audited_draft_hash": computed_hash,
                "declared_hash_matches": draft.get("audited_draft_hash") == computed_hash,
                "receipt_matches": args.receipt is not None,
                "evidence_pack_checked": args.evidence_pack is not None,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
