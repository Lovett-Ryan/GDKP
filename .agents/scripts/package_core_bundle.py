#!/usr/bin/env python3
"""Materialize an atomic project-local snapshot of the complete core Skill bundle."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile


BUNDLE_VERSION = "1.1.0"
COPY_DIRECTORIES = ("skills", "references", "scripts")


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inventory(root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    for directory_name in COPY_DIRECTORIES:
        directory = root / directory_name
        if not directory.is_dir():
            raise ValueError(f"source bundle is missing {directory_name}/")
        for path in sorted(directory.rglob("*")):
            if not path.is_file() or "__pycache__" in path.parts or path.suffix == ".pyc":
                continue
            relative = path.relative_to(root).as_posix()
            files[relative] = file_digest(path)
    return files


def tree_digest(files: dict[str, str]) -> str:
    digest = hashlib.sha256()
    for relative, value in sorted(files.items()):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(value.encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def bundled_skill_versions(root: Path) -> dict[str, str]:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        raise ValueError("source bundle is missing skills/")
    return {
        path.name: BUNDLE_VERSION
        for path in sorted(skills_root.iterdir())
        if path.is_dir() and (path / "SKILL.md").is_file()
    }


def copy_bundle(source: Path, staging: Path) -> None:
    for directory_name in COPY_DIRECTORIES:
        shutil.copytree(
            source / directory_name,
            staging / directory_name,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "destination",
        type=Path,
        help="non-existent destination root, normally a staged .agents directory",
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument(
        "--source-id",
        default="goal-driven-knowledge-product-core",
        help="version-control or release identity recorded in the manifest",
    )
    args = parser.parse_args()
    source = args.source_root.resolve()
    destination = args.destination.resolve()
    if destination.exists():
        print("ERROR: destination already exists; refusing to merge or overwrite", file=sys.stderr)
        return 2
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        source_files = inventory(source)
        staging = Path(
            tempfile.mkdtemp(
                prefix=f".{destination.name}.staging-", dir=destination.parent
            )
        )
        try:
            copy_bundle(source, staging)
            installed_files = inventory(staging)
            if installed_files != source_files:
                raise ValueError("staged bundle inventory differs from the source inventory")
            manifest = {
                "schema_version": 1,
                "bundle_version": BUNDLE_VERSION,
                "skill_versions": bundled_skill_versions(source),
                "source_id": args.source_id,
                "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "tree_sha256": tree_digest(installed_files),
                "files": installed_files,
            }
            (staging / "core-bundle-manifest.yaml").write_text(
                json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            os.replace(staging, destination)
        except Exception:
            shutil.rmtree(staging, ignore_errors=True)
            raise
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "bundle_version": BUNDLE_VERSION,
                "destination": str(destination),
                "file_count": len(source_files),
                "tree_sha256": tree_digest(source_files),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
