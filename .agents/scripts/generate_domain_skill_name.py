#!/usr/bin/env python3
"""Generate governed canonical and UI names for a project-scoped domain skill."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys


SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SOURCE_LABEL = re.compile(
    r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@[0-9a-f]{7,12}$"
)
MAX_NAME_LENGTH = 64


def validate_display(label: str, value: str, *, allow_brackets: bool = True) -> str:
    if not value or value != value.strip():
        raise ValueError(f"{label} must be non-empty and cannot have outer whitespace")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        raise ValueError(f"{label} cannot contain control characters")
    if not value.isascii():
        raise ValueError(f"{label} must use an approved English ASCII alias")
    if not allow_brackets and ("[" in value or "]" in value):
        raise ValueError(f"{label} cannot contain square brackets")
    return value


def balanced_prefix(segments: tuple[str, ...], budget: int) -> str:
    separator_cost = len(segments) - 1
    character_budget = budget - separator_cost
    if character_budget < len(segments):
        raise ValueError("the canonical name budget cannot preserve every segment")
    allocations = [1 for _ in segments]
    remaining = character_budget - len(segments)
    while remaining:
        expandable = [
            index for index, segment in enumerate(segments) if allocations[index] < len(segment)
        ]
        if not expandable:
            break
        expandable.sort(
            key=lambda index: (len(segments[index]) - allocations[index], -index),
            reverse=True,
        )
        for index in expandable:
            if not remaining:
                break
            allocations[index] += 1
            remaining -= 1
    readable_segments = [
        segment[:allocation].rstrip("-") for segment, allocation in zip(segments, allocations)
    ]
    if any(not segment for segment in readable_segments):
        raise ValueError("the canonical name cannot retain every readable segment")
    return "-".join(readable_segments)


def source_short_description(source_label: str) -> str:
    if not SOURCE_LABEL.fullmatch(source_label):
        raise ValueError("source label must use owner/repo@short-commit")
    prefix = "GitHub Skill: "
    if len(prefix + source_label) <= 64:
        return prefix + source_label
    repository, commit = source_label.rsplit("@", 1)
    suffix = f"~{hashlib.sha256(source_label.encode('utf-8')).hexdigest()[:6]}@{commit}"
    readable_budget = 64 - len(prefix) - len(suffix)
    readable_repository = repository[:readable_budget].rstrip("-._/")
    if "/" not in readable_repository:
        raise ValueError("source label is too long to preserve owner/repository identity")
    return prefix + readable_repository + suffix


def build_name(project: str, field: str, upstream: str, source: str, collision: bool) -> str:
    for label, value in (("project", project), ("field", field), ("upstream", upstream)):
        if not SLUG.fullmatch(value):
            raise ValueError(f"{label} slug is invalid: {value!r}")
    base = f"{project}-{field}-{upstream}"
    if len(base) <= MAX_NAME_LENGTH and not collision:
        return base
    suffix = hashlib.sha256(source.encode("utf-8")).hexdigest()[:8]
    prefix_length = MAX_NAME_LENGTH - len(suffix) - 1
    prefix = balanced_prefix((project, field, upstream), prefix_length)
    return f"{prefix}-{suffix}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-slug", required=True)
    parser.add_argument("--field-slug", required=True)
    parser.add_argument("--upstream-slug", required=True)
    parser.add_argument("--project-display", required=True)
    parser.add_argument("--field-display", required=True)
    parser.add_argument("--upstream-display", required=True)
    parser.add_argument("--source-identity", required=True, help="repository, path, and commit identity")
    parser.add_argument(
        "--source-label", required=True, help="front-end provenance in owner/repo@short-commit form"
    )
    parser.add_argument("--collision", action="store_true")
    args = parser.parse_args()
    try:
        if not args.source_identity.strip():
            raise ValueError("source identity must be non-empty")
        project_display = validate_display(
            "project display name", args.project_display, allow_brackets=False
        )
        field_display = validate_display(
            "field display name", args.field_display, allow_brackets=False
        )
        upstream_display = validate_display("upstream display name", args.upstream_display)
        short_description = source_short_description(args.source_label)
        canonical = build_name(
            args.project_slug,
            args.field_slug,
            args.upstream_slug,
            args.source_identity,
            args.collision,
        )
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    result = {
        "canonical_name": canonical,
        "display_name": f"[{project_display}]-[{field_display}] {upstream_display}",
        "short_description": short_description,
        "default_prompt_skill_token": f"${canonical}",
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
