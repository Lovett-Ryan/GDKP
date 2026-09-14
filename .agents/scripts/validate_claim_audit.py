#!/usr/bin/env python3
"""Compute a DraftClaimSet hash and optionally validate its ClaimAuditReceipt."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


PASSING_AUDIT_STATUSES = {"passed", "passed_with_caveat"}
PASSING_RESULTS = {"direct", "partial"}


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


def validate_receipt(
    draft: dict[str, Any], receipt: dict[str, Any], computed_hash: str
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
        "--require-declared-hash",
        action="store_true",
        help="fail unless the draft declares the computed hash",
    )
    args = parser.parse_args()
    try:
        draft = unwrap(load_object(args.draft), "draft_claim_set")
        computed_hash = compute_hash(draft)
        errors: list[str] = []
        if args.require_declared_hash and draft.get("audited_draft_hash") != computed_hash:
            errors.append("DraftClaimSet audited_draft_hash does not match canonical content")
        if args.receipt is not None:
            receipt = unwrap(load_object(args.receipt), "claim_audit_receipt")
            errors.extend(validate_receipt(draft, receipt, computed_hash))
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
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
