#!/usr/bin/env python3
"""Score declared GitHub domain-skill candidates using the governed rubric."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from pathlib import PurePosixPath


MAXIMUMS = {
    "goal_and_domain_fit": 25,
    "professional_rigor": 20,
    "safety_and_least_authority": 20,
    "source_and_maintenance_credibility": 15,
    "verifiability": 10,
    "license_and_portability": 10,
}
UUID7 = re.compile(
    r"^dsc_[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
GITHUB_REPOSITORY = re.compile(r"^https://github\.com/[^/\s]+/[^/\s]+(?:\.git)?/?$")
RESOLVED_COMMIT = re.compile(r"^[0-9a-fA-F]{7,64}$")
SOURCE_FIELDS = (
    "repo_url",
    "repo_path",
    "upstream_author",
    "upstream_name",
    "upstream_display_name",
    "requested_ref",
    "resolved_commit",
    "license",
)


def validate_source(candidate_id: str, source: object) -> None:
    if not isinstance(source, dict):
        raise ValueError(f"{candidate_id}: source must be an object")
    missing = [
        field
        for field in SOURCE_FIELDS
        if not isinstance(source.get(field), str) or not source[field].strip()
    ]
    if missing:
        raise ValueError(
            f"{candidate_id}: missing source provenance fields: {', '.join(missing)}"
        )
    if not GITHUB_REPOSITORY.fullmatch(source["repo_url"]):
        raise ValueError(f"{candidate_id}: source.repo_url must identify a GitHub repository")
    repo_path = PurePosixPath(source["repo_path"])
    if repo_path.is_absolute() or ".." in repo_path.parts or source["repo_path"] in {".", ""}:
        raise ValueError(f"{candidate_id}: source.repo_path must be a safe relative path")
    if not RESOLVED_COMMIT.fullmatch(source["resolved_commit"]):
        raise ValueError(f"{candidate_id}: source.resolved_commit must be a fixed hexadecimal commit")


def score_candidate(candidate: dict) -> dict:
    if not isinstance(candidate, dict):
        raise ValueError("each candidate must be an object")
    candidate_id = candidate.get("candidate_id")
    if not isinstance(candidate_id, str) or not UUID7.fullmatch(candidate_id):
        raise ValueError("each candidate_id must be dsc_<UUIDv7>")
    validate_source(candidate_id, candidate.get("source"))
    scores = candidate.get("score")
    if not isinstance(scores, dict):
        raise ValueError(f"{candidate_id}: score must be an object")
    supplied_dimensions = set(scores) - {"total"}
    missing_dimensions = sorted(set(MAXIMUMS) - supplied_dimensions)
    unexpected_dimensions = sorted(supplied_dimensions - set(MAXIMUMS))
    if missing_dimensions:
        raise ValueError(
            f"{candidate_id}: missing score dimensions: {', '.join(missing_dimensions)}"
        )
    if unexpected_dimensions:
        raise ValueError(
            f"{candidate_id}: unexpected score dimensions: {', '.join(unexpected_dimensions)}"
        )
    normalized: dict[str, float] = {}
    for dimension, maximum in MAXIMUMS.items():
        value = scores.get(dimension)
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"{candidate_id}: {dimension} must be numeric")
        value = float(value)
        if not 0 <= value <= maximum:
            raise ValueError(f"{candidate_id}: {dimension} must be between 0 and {maximum}")
        normalized[dimension] = value
    vetoes = candidate.get("vetoes", [])
    if not isinstance(vetoes, list) or not all(isinstance(item, str) for item in vetoes):
        raise ValueError(f"{candidate_id}: vetoes must be a string list")
    total = round(sum(normalized.values()), 3)
    checks = {
        "total_at_least_75": total >= 75,
        "goal_and_domain_fit_at_least_18": normalized["goal_and_domain_fit"] >= 18,
        "safety_and_least_authority_at_least_15": normalized[
            "safety_and_least_authority"
        ]
        >= 15,
        "no_vetoes": not vetoes,
    }
    result = dict(candidate)
    result["score"] = {**normalized, "total": total}
    result["eligibility_checks"] = checks
    result["eligible"] = all(checks.values())
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("document", type=Path, help="JSON document with a candidates array")
    parser.add_argument("--limit", type=int, default=3, help="maximum eligible candidates to return")
    args = parser.parse_args()
    if not 1 <= args.limit <= 3:
        print("ERROR: --limit must be between 1 and 3", file=sys.stderr)
        return 2
    try:
        data = json.loads(args.document.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("document root must be an object")
        manifest = data.get("domain_skill_candidate_manifest")
        if not isinstance(manifest, dict):
            raise ValueError("document requires domain_skill_candidate_manifest")
        candidates = manifest.get("candidates") if isinstance(manifest, dict) else None
        if not isinstance(candidates, list):
            raise ValueError("document requires a candidates array")
        scored = [score_candidate(candidate) for candidate in candidates]
        candidate_ids = [candidate["candidate_id"] for candidate in scored]
        if len(candidate_ids) != len(set(candidate_ids)):
            raise ValueError("candidate_id values must be unique")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    ranked = sorted(
        scored, key=lambda item: (-item["score"]["total"], item["candidate_id"])
    )
    eligible = [item for item in ranked if item["eligible"]][: args.limit]
    output = {"eligible_candidates": eligible, "all_candidates": ranked}
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
