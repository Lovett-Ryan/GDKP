#!/usr/bin/env python3
"""Validate a reader-facing citation projection before publication."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any
from urllib.parse import urlparse


SHA256 = re.compile(r"^[0-9a-f]{64}$")
INLINE_CITATION = re.compile(r"(?<!\\)\[(\d+)\]")
REFERENCE_HEADING = re.compile(
    r"^(#{1,6})\s+(References|Reference|Bibliography|\u53c2\u8003\u6587\u732e)\s*$",
    re.IGNORECASE,
)
REFERENCE_LINE = re.compile(r"^\s*(?:\[(\d+)\]|(\d+)\.)\s+(.+?)\s*$")
FORBIDDEN_VISIBLE_PATTERNS = (
    re.compile(r"Zotero\s*:", re.IGNORECASE),
    re.compile(r"\bEvidenceUnit\b", re.IGNORECASE),
    re.compile(r"\bevu_[A-Za-z0-9_-]+\b"),
    re.compile(r"\bclaim_[A-Za-z0-9_-]+\b"),
)
SOURCE_IDENTITY_KEYS = (
    "zotero_item_key",
    "source_id",
    "source_record_id",
    "doi",
    "isbn",
    "url",
    "commit_hash",
)
INTERNAL_ONLY_IDENTITY_KEYS = {
    "zotero_item_key",
    "source_id",
    "source_record_id",
    "commit_hash",
}


def load_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: document root must be an object")
    return value


def unwrap(value: dict[str, Any], key: str) -> dict[str, Any]:
    nested = value.get(key, value)
    if not isinstance(nested, dict):
        raise ValueError(f"{key} must be an object")
    return nested


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_identity(value: Any) -> tuple[str, str] | None:
    if not isinstance(value, dict):
        return None
    nested = value.get("source_identity")
    source = nested if isinstance(nested, dict) else value
    for key in SOURCE_IDENTITY_KEYS:
        candidate = source.get(key)
        if isinstance(candidate, str) and candidate.strip():
            return key, candidate.strip()
    return None


def evidence_unit_id(value: dict[str, Any]) -> str | None:
    for key in ("evidence_unit_id", "unit_id", "id"):
        candidate = value.get(key)
        if isinstance(candidate, str) and candidate:
            return candidate
    return None


def split_reference_section(text: str) -> tuple[str, str | None, list[str]]:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        match = REFERENCE_HEADING.match(line.strip())
        if not match:
            continue
        level = len(match.group(1))
        end = len(lines)
        for candidate_index in range(index + 1, len(lines)):
            heading = re.match(r"^(#{1,6})\s+", lines[candidate_index].strip())
            if heading and len(heading.group(1)) <= level:
                end = candidate_index
                break
        body = "\n".join(lines[:index])
        return body, line.strip(), lines[index + 1 : end]
    return text, None, []


def normalize_space(value: str) -> str:
    return " ".join(value.split())


def validate_url(value: Any, label: str, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        return
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        errors.append(f"{label} must be an absolute HTTP(S) URL")


def expected_sources(
    draft_claims: dict[str, Any] | None,
    evidence_pack: dict[str, Any] | None,
) -> tuple[dict[tuple[str, str], set[str]], list[str]]:
    errors: list[str] = []
    if draft_claims is None or evidence_pack is None:
        return {}, errors
    claims = draft_claims.get("claims")
    units = evidence_pack.get("evidence_units")
    if not isinstance(claims, list) or not all(isinstance(item, dict) for item in claims):
        return {}, ["DraftClaimSet claims must be an object list"]
    if not isinstance(units, list) or not all(isinstance(item, dict) for item in units):
        return {}, ["EvidencePack evidence_units must be an object list"]
    units_by_id = {
        evidence_unit_id(unit): unit
        for unit in units
        if evidence_unit_id(unit) is not None
    }
    result: dict[tuple[str, str], set[str]] = {}
    for claim in claims:
        claim_id = claim.get("claim_id")
        evidence_ids = claim.get("evidence_unit_ids")
        if not isinstance(claim_id, str) or not claim_id:
            errors.append("DraftClaimSet contains a claim without claim_id")
            continue
        if not isinstance(evidence_ids, list) or not evidence_ids:
            errors.append(f"DraftClaimSet claim {claim_id} requires EvidenceUnits")
            continue
        for unit_id in evidence_ids:
            unit = units_by_id.get(unit_id)
            if unit is None:
                errors.append(f"DraftClaimSet claim {claim_id} references unknown EvidenceUnit {unit_id}")
                continue
            identity = source_identity(unit)
            if identity is None:
                errors.append(f"EvidenceUnit {unit_id} has no concrete source identity")
                continue
            result.setdefault(identity, set()).add(claim_id)
    return result, errors


def validate_projection(
    draft_text: str,
    source_draft_text: str,
    manifest: dict[str, Any],
    draft_claims: dict[str, Any] | None,
    evidence_pack: dict[str, Any] | None,
) -> tuple[list[str], dict[str, Any]]:
    errors: list[str] = []
    if manifest.get("artifact_type") != "CitationProjection":
        errors.append("manifest artifact_type must be CitationProjection")
    declared_hash = manifest.get("projected_draft_sha256")
    computed_hash = sha256_text(draft_text)
    if declared_hash != computed_hash:
        errors.append("manifest projected_draft_sha256 does not match the draft")
    source_hash = manifest.get("source_draft_sha256")
    if not isinstance(source_hash, str) or not SHA256.fullmatch(source_hash):
        errors.append("manifest source_draft_sha256 must be lowercase SHA-256 hex")
    elif source_hash != sha256_text(source_draft_text):
        errors.append("manifest source_draft_sha256 does not match the source draft")

    for pattern in FORBIDDEN_VISIBLE_PATTERNS:
        if pattern.search(draft_text):
            errors.append(f"reader-facing draft exposes internal marker matching {pattern.pattern}")

    entries = manifest.get("entries")
    if not isinstance(entries, list) or not all(isinstance(item, dict) for item in entries):
        errors.append("manifest entries must be an object list")
        entries = []

    numbers: list[int] = []
    manifest_sources: dict[tuple[str, str], set[str]] = {}
    entries_by_number: dict[int, dict[str, Any]] = {}
    for entry in entries:
        number = entry.get("number")
        if not isinstance(number, int) or isinstance(number, bool) or number <= 0:
            errors.append("every citation entry requires a positive integer number")
            continue
        numbers.append(number)
        if number in entries_by_number:
            errors.append(f"citation number {number} is duplicated")
        entries_by_number[number] = entry
        identity = source_identity(entry)
        if identity is None:
            errors.append(f"citation {number} requires a concrete source_identity")
        else:
            if identity in manifest_sources:
                errors.append(f"source identity {identity[1]} is assigned more than one number")
            claim_ids = entry.get("claim_ids", [])
            if not isinstance(claim_ids, list) or not all(
                isinstance(item, str) and item for item in claim_ids
            ):
                errors.append(f"citation {number} claim_ids must be a string list")
                claim_ids = []
            manifest_sources[identity] = set(claim_ids)
            if identity[0] in INTERNAL_ONLY_IDENTITY_KEYS and identity[1] in draft_text:
                errors.append(f"reader-facing draft exposes internal source identity {identity[1]}")
        reference_text = entry.get("reference_text")
        if not isinstance(reference_text, str) or not reference_text.strip():
            errors.append(f"citation {number} requires reference_text")
        validate_url(entry.get("original_url"), f"citation {number} original_url", errors)

    expected_numbers = list(range(1, len(entries) + 1))
    if sorted(numbers) != expected_numbers:
        errors.append("citation numbers must be unique and contiguous from 1")

    body, reference_heading, reference_lines = split_reference_section(draft_text)
    body_numbers = {int(value) for value in INLINE_CITATION.findall(body)}
    reference_rows: dict[int, str] = {}
    for line in reference_lines:
        match = REFERENCE_LINE.match(line)
        if not match:
            continue
        number = int(match.group(1) or match.group(2))
        if number in reference_rows:
            errors.append(f"reference entry {number} is duplicated")
        reference_rows[number] = match.group(3)

    manifest_numbers = set(entries_by_number)
    if entries and reference_heading is None:
        errors.append("reader-facing draft requires a References section")
    if body_numbers != manifest_numbers:
        errors.append("inline citation numbers do not exactly match the CitationProjection")
    if set(reference_rows) != manifest_numbers:
        errors.append("References entries do not exactly match the CitationProjection")

    for number, entry in entries_by_number.items():
        row = reference_rows.get(number)
        if row is None:
            continue
        reference_text = entry.get("reference_text")
        if isinstance(reference_text, str) and normalize_space(reference_text) not in normalize_space(row):
            errors.append(f"reference entry {number} does not contain its formatted reference_text")
        original_url = entry.get("original_url")
        if isinstance(original_url, str) and original_url:
            if f"]({original_url})" not in row:
                errors.append(f"reference entry {number} lacks a clickable original_url")

    required_sources, source_errors = expected_sources(draft_claims, evidence_pack)
    errors.extend(source_errors)
    if required_sources:
        if set(manifest_sources) != set(required_sources):
            missing = sorted(identity[1] for identity in set(required_sources) - set(manifest_sources))
            extra = sorted(identity[1] for identity in set(manifest_sources) - set(required_sources))
            if missing:
                errors.append("CitationProjection is missing audited sources: " + ", ".join(missing))
            if extra:
                errors.append("CitationProjection contains unaudited numbered sources: " + ", ".join(extra))
        for identity in set(required_sources) & set(manifest_sources):
            if manifest_sources[identity] != required_sources[identity]:
                errors.append(
                    f"CitationProjection claim_ids do not match audited evidence for {identity[1]}"
                )

    return errors, {
        "citation_count": len(entries),
        "inline_number_count": len(body_numbers),
        "reference_count": len(reference_rows),
        "projected_draft_sha256": computed_hash,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="reader-facing projected Markdown draft")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--source-draft", required=True, type=Path)
    parser.add_argument("--draft-claims", type=Path)
    parser.add_argument("--evidence-pack", type=Path)
    args = parser.parse_args()
    if bool(args.draft_claims) != bool(args.evidence_pack):
        print("ERROR: --draft-claims and --evidence-pack must be supplied together", file=sys.stderr)
        return 2
    try:
        draft_text = args.draft.read_text(encoding="utf-8")
        source_draft_text = args.source_draft.read_text(encoding="utf-8")
        manifest = unwrap(load_object(args.manifest), "citation_projection")
        draft_claims = (
            unwrap(load_object(args.draft_claims), "draft_claim_set")
            if args.draft_claims
            else None
        )
        evidence_pack = (
            unwrap(load_object(args.evidence_pack), "evidence_pack")
            if args.evidence_pack
            else None
        )
        errors, summary = validate_projection(
            draft_text, source_draft_text, manifest, draft_claims, evidence_pack
        )
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in dict.fromkeys(errors):
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    summary["valid"] = True
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
