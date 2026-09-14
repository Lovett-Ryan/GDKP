#!/usr/bin/env python3
"""Regression tests for deterministic bundle helpers."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / ".agents"
SCRIPTS = BUNDLE / "scripts"
FIXTURES = ROOT / "tests" / "fixtures"


def run_script(name: str, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *arguments],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def write_json(directory: Path, name: str, payload: object) -> Path:
    path = directory / name
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


class BundleValidationTests(unittest.TestCase):
    def validate_snapshot(self, destination: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(destination / "scripts" / "validate_bundle.py"),
                str(destination),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_bundle_is_valid(self) -> None:
        result = run_script("validate_bundle.py", str(BUNDLE))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Validated 13 skills", result.stdout)

    def test_project_local_bundle_snapshot_preserves_dependencies(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / ".agents"
            packaged = run_script(
                "package_core_bundle.py",
                str(destination),
                "--source-id",
                "test-source@01234567",
            )
            self.assertEqual(packaged.returncode, 0, packaged.stderr)
            manifest_path = destination / "core-bundle-manifest.yaml"
            self.assertTrue(manifest_path.is_file())
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["bundle_version"], "1.0.0")
            self.assertEqual(len(manifest["skill_versions"]), 13)
            self.assertEqual(set(manifest["skill_versions"].values()), {"1.0.0"})
            self.assertTrue((destination / "references" / "workflow-contracts.md").is_file())
            self.assertTrue((destination / "scripts" / "validate_bundle.py").is_file())
            self.assertTrue(
                (
                    destination
                    / "skills"
                    / "notion-natural-prose-editor"
                    / "SKILL.md"
                ).is_file()
            )
            validated = self.validate_snapshot(destination)
        self.assertEqual(validated.returncode, 0, validated.stderr)

    def test_manifest_detects_core_file_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / ".agents"
            packaged = run_script("package_core_bundle.py", str(destination))
            self.assertEqual(packaged.returncode, 0, packaged.stderr)
            skill_path = destination / "skills" / "knowledge-product-orchestrator" / "SKILL.md"
            skill_path.write_text(
                skill_path.read_text(encoding="utf-8") + "\nA tampered line.\n",
                encoding="utf-8",
            )
            result = self.validate_snapshot(destination)
        self.assertEqual(result.returncode, 1)
        self.assertIn("digest mismatch", result.stderr)

    def test_manifest_detects_unsynchronized_skill_version(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / ".agents"
            packaged = run_script("package_core_bundle.py", str(destination))
            self.assertEqual(packaged.returncode, 0, packaged.stderr)
            manifest_path = destination / "core-bundle-manifest.yaml"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["skill_versions"]["knowledge-product-orchestrator"] = "1.0.1"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            result = self.validate_snapshot(destination)
        self.assertEqual(result.returncode, 1)
        self.assertIn("skill versions must match bundle version", result.stderr)

    def test_governed_project_domain_skill_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / ".agents"
            packaged = run_script("package_core_bundle.py", str(destination))
            self.assertEqual(packaged.returncode, 0, packaged.stderr)
            name = "bridge-audit-engineering-standards-example"
            skill_dir = destination / "skills" / name
            (skill_dir / "agents").mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                f"name: {name}\n"
                "description: Apply the approved engineering standard method for this project only.\n"
                "---\n\n# Project Method\n\nUse only the approved project inputs.\n",
                encoding="utf-8",
            )
            (skill_dir / "agents" / "openai.yaml").write_text(
                "interface:\n"
                "  display_name: \"[Bridge Audit]-[Engineering Standards] Example\"\n"
                "  short_description: \"GitHub Skill: owner/repo@01234567\"\n"
                f"  default_prompt: \"Use ${name} for the approved method.\"\n",
                encoding="utf-8",
            )
            kernel = root / ".knowledge-product"
            kernel.mkdir()
            write_json(
                kernel,
                "domain-skills.lock.yaml",
                {
                    "domain_skills": [
                        {
                            "status": "active",
                            "naming": {
                                "canonical_name": name,
                                "local_path": f".agents/skills/{name}",
                            },
                        }
                    ]
                },
            )
            result = self.validate_snapshot(destination)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_non_latin_script_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / ".agents"
            packaged = run_script("package_core_bundle.py", str(destination))
            self.assertEqual(packaged.returncode, 0, packaged.stderr)
            skill_path = destination / "skills" / "knowledge-product-orchestrator" / "SKILL.md"
            skill_path.write_text(
                skill_path.read_text(encoding="utf-8")
                + "\n"
                + chr(0x0422)
                + "est in a non-Latin script.\n",
                encoding="utf-8",
            )
            result = self.validate_snapshot(destination)
        self.assertEqual(result.returncode, 1)
        self.assertIn("non-English script character", result.stderr)


class CoverageAuditValidationTests(unittest.TestCase):
    def load_valid_audit(self) -> dict:
        return json.loads(
            (FIXTURES / "valid-coverage-audit.json").read_text(encoding="utf-8")
        )

    def test_valid_coverage_audit_passes(self) -> None:
        result = run_script(
            "validate_coverage_audit.py",
            str(FIXTURES / "valid-coverage-audit.json"),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertTrue(summary["valid"])
        self.assertEqual(summary["topic_count"], 3)
        self.assertEqual(summary["mapped_topic_count"], 3)

    def test_authorized_local_structural_file_supports_degraded_verification(self) -> None:
        payload = self.load_valid_audit()
        audit = payload["coverage_audit"]
        audit["status"] = "coverage_local_verified"
        audit["baseline"]["status"] = "local_files_verified"
        source = audit["baseline"]["sources"][0]
        source.update(
            {
                "status": "local_files_verified",
                "location_ref": "/approved/reference-toc.pdf",
                "content_sha256": "a" * 64,
                "extraction_method": "pdftotext-plus-visual-readback",
                "readback_verified": True,
                "authorization": {
                    "kind": "user",
                    "ref": "conversation:user:attached-reference",
                },
            }
        )
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(Path(temporary), "local-verified.json", payload)
            result = run_script("validate_coverage_audit.py", str(path))
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["status"], "coverage_local_verified")
        self.assertEqual(summary["local_source_count"], 1)

    def test_local_structural_file_cannot_claim_full_verification(self) -> None:
        payload = self.load_valid_audit()
        audit = payload["coverage_audit"]
        audit["baseline"]["status"] = "local_files_verified"
        source = audit["baseline"]["sources"][0]
        source.update(
            {
                "status": "local_files_verified",
                "location_ref": "/approved/reference-toc.pdf",
                "content_sha256": "not-a-digest",
                "extraction_method": "pdftotext",
                "readback_verified": True,
                "authorization": {
                    "kind": "user",
                    "ref": "conversation:user:attached-reference",
                },
            }
        )
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(Path(temporary), "invalid-local-promotion.json", payload)
            result = run_script("validate_coverage_audit.py", str(path))
        self.assertEqual(result.returncode, 1)
        self.assertIn("content_sha256 must be a lowercase SHA-256", result.stderr)
        self.assertIn("coverage_verified cannot rely", result.stderr)

    def test_missing_baseline_topic_fails(self) -> None:
        payload = self.load_valid_audit()
        payload["coverage_audit"]["matrix"]["mappings"].pop()
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(Path(temporary), "missing-topic.json", payload)
            result = run_script("validate_coverage_audit.py", str(path))
        self.assertEqual(result.returncode, 1)
        self.assertIn("baseline topics missing from matrix", result.stderr)

    def test_ai_cannot_silently_narrow_scope(self) -> None:
        payload = self.load_valid_audit()
        decision = payload["coverage_audit"]["scope_decisions"][1]
        decision["authority"] = {"kind": "ai", "ref": "model-judgment"}
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(Path(temporary), "silent-narrowing.json", payload)
            result = run_script("validate_coverage_audit.py", str(path))
        self.assertEqual(result.returncode, 1)
        self.assertIn("silently narrows scope with AI authority", result.stderr)

    def test_omission_requires_accountable_authority(self) -> None:
        payload = self.load_valid_audit()
        omission = payload["coverage_audit"]["omission_ledger"]["omissions"][0]
        omission["authority"] = {"kind": "ai", "ref": "shorter-outline"}
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(Path(temporary), "unaccountable-omission.json", payload)
            result = run_script("validate_coverage_audit.py", str(path))
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires user, policy, or structural_evidence authority", result.stderr)

    def test_mastery_requires_framework_target(self) -> None:
        payload = self.load_valid_audit()
        mapping = payload["coverage_audit"]["matrix"]["mappings"][1]
        mapping["target_refs"] = []
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(Path(temporary), "missing-target.json", payload)
            result = run_script("validate_coverage_audit.py", str(path))
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires at least one framework target", result.stderr)

    def test_coverage_contract_must_bind_current_baseline(self) -> None:
        payload = self.load_valid_audit()
        payload["coverage_audit"]["coverage_contract"]["baseline_id"] = "stale-baseline"
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(Path(temporary), "stale-contract.json", payload)
            result = run_script("validate_coverage_audit.py", str(path))
        self.assertEqual(result.returncode, 1)
        self.assertIn("coverage_contract.baseline_id does not match", result.stderr)

    def test_deep_learning_regression_catches_unknown_missing_branches(self) -> None:
        payload = self.load_valid_audit()
        topics = payload["coverage_audit"]["baseline"]["topics"]
        topics.extend(
            [
                {
                    "topic_id": "topic-sampling",
                    "title": "Sampling methods",
                    "importance": "important",
                    "dependency_ids": ["topic-math"],
                },
                {
                    "topic_id": "topic-latent-variables",
                    "title": "Latent-variable models",
                    "importance": "important",
                    "dependency_ids": ["topic-math"],
                },
            ]
        )
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(Path(temporary), "deep-learning-regression.json", payload)
            result = run_script("validate_coverage_audit.py", str(path))
        self.assertEqual(result.returncode, 1)
        self.assertIn("topic-sampling", result.stderr)
        self.assertIn("topic-latent-variables", result.stderr)


class HandoffValidationTests(unittest.TestCase):
    def test_valid_fixture_passes(self) -> None:
        result = run_script(
            "validate_handoff.py", str(FIXTURES / "valid-handoff.json")
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_natural_prose_revision_handoff_is_core_owned(self) -> None:
        payload = json.loads((FIXTURES / "valid-handoff.json").read_text(encoding="utf-8"))
        handoff = payload["handoff"]
        handoff["producer_skill"] = "notion-natural-prose-editor"
        handoff["stage"] = "composing"
        handoff["artifacts"][0].update(
            {
                "artifact_type": "NaturalProseRevisionMemo",
                "artifact_id": "npm_01991d8e-1234-7abc-8def-3234567890ab",
                "uri": ".knowledge-product/artifacts/notion-natural-prose-revision-memo.json",
                "producer_skill": "notion-natural-prose-editor",
                "status": "verified",
            }
        )
        handoff["artifact_schema_versions"] = {"NaturalProseRevisionMemo": 1}
        handoff["next_skill"] = "notion-node-author"
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(Path(temporary), "natural-prose-handoff.json", payload)
            result = run_script("validate_handoff.py", str(path))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_mode_and_digest_fail_cleanly(self) -> None:
        payload = json.loads((FIXTURES / "valid-handoff.json").read_text(encoding="utf-8"))
        payload["handoff"]["mode"] = "research"
        payload["handoff"]["artifacts"][0]["sha256"] = "not-a-digest"
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(Path(temporary), "invalid-handoff.json", payload)
            result = run_script("validate_handoff.py", str(path))
        self.assertEqual(result.returncode, 1)
        self.assertIn("invalid mode", result.stderr)
        self.assertIn("lowercase SHA-256", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_malformed_types_stage_identity_and_owner_fail_cleanly(self) -> None:
        payload = json.loads((FIXTURES / "valid-handoff.json").read_text(encoding="utf-8"))
        handoff = payload["handoff"]
        handoff["mode"] = []
        handoff["stage"] = "totally_invalid"
        handoff["project_id"] = "prj_not-a-uuid"
        handoff["artifacts"][0]["producer_skill"] = "notion-node-author"
        handoff["artifacts"][0]["status"] = "fabricated"
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(Path(temporary), "invalid-semantics.json", payload)
            result = run_script("validate_handoff.py", str(path))
        self.assertEqual(result.returncode, 1)
        self.assertIn("invalid mode", result.stderr)
        self.assertIn("invalid stage", result.stderr)
        self.assertIn("prj_<UUIDv7>", result.stderr)
        self.assertIn("must be produced by intent-source-analysis", result.stderr)
        self.assertIn("invalid artifact status", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_project_domain_skill_name_is_structurally_valid(self) -> None:
        payload = json.loads((FIXTURES / "valid-handoff.json").read_text(encoding="utf-8"))
        handoff = payload["handoff"]
        handoff["producer_skill"] = (
            "bridge-audit-engineering-standards-eurocode-assistant"
        )
        handoff["artifacts"] = []
        handoff["artifact_schema_versions"] = {}
        handoff["next_skill"] = "outcome-orchestrator"
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(Path(temporary), "domain-handoff.json", payload)
            result = run_script("validate_handoff.py", str(path))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_malformed_artifact_type_fails_without_traceback(self) -> None:
        payload = json.loads((FIXTURES / "valid-handoff.json").read_text(encoding="utf-8"))
        payload["handoff"]["artifacts"][0]["artifact_type"] = []
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(Path(temporary), "invalid-artifact-type.json", payload)
            result = run_script("validate_handoff.py", str(path))
        self.assertEqual(result.returncode, 1)
        self.assertIn("artifact_type must be a non-empty string", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


class ClaimAuditValidationTests(unittest.TestCase):
    def build_draft(self) -> dict:
        return {
            "draft_claim_set": {
                "draft_claim_set_id": "dcs_01991d8e-1234-7abc-8def-5234567890ab",
                "project_id": "prj_01991d8e-1234-7abc-8def-1234567890ab",
                "target_ref": {
                    "kind": "knowledge_node",
                    "id": "kn_01991d8e-1234-7abc-8def-6234567890ab",
                },
                "framework_revision": 1,
                "framework_diff_hash": None,
                "evidence_pack_id": "epk_01991d8e-1234-7abc-8def-7234567890ab",
                "evidence_pack_checksum": "1" * 64,
                "source_revisions": {"src_example": "rev-1"},
                "claims": [
                    {
                        "claim_id": "clm_01991d8e-1234-7abc-8def-8234567890ab",
                        "target_path": "sections.definition",
                        "exact_text": "A bounded test claim.",
                        "claim_kind": "definition",
                        "evidence_unit_ids": [
                            "evu_01991d8e-1234-7abc-8def-9234567890ab"
                        ],
                        "citation_uids": [
                            "cit_01991d8e-1234-7abc-8def-a234567890ab"
                        ],
                        "required_support": "direct",
                    }
                ],
                "combination_reservations": [],
                "non_claim_content_hash": "2" * 64,
                "canonicalization": "jcs",
                "audited_draft_hash": "",
            }
        }

    def test_exact_draft_receipt_passes_and_drift_fails(self) -> None:
        draft = self.build_draft()
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            draft_path = write_json(directory, "draft.json", draft)
            computed = run_script("validate_claim_audit.py", str(draft_path))
            self.assertEqual(computed.returncode, 0, computed.stderr)
            digest = json.loads(computed.stdout)["audited_draft_hash"]
            draft["draft_claim_set"]["audited_draft_hash"] = digest
            draft_path = write_json(directory, "draft.json", draft)
            receipt = {
                "claim_audit_receipt": {
                    "audit_receipt_id": "car_01991d8e-1234-7abc-8def-b234567890ab",
                    "draft_claim_set_id": draft["draft_claim_set"]["draft_claim_set_id"],
                    "audited_draft_hash": digest,
                    "evidence_pack_id": draft["draft_claim_set"]["evidence_pack_id"],
                    "evidence_pack_checksum": draft["draft_claim_set"][
                        "evidence_pack_checksum"
                    ],
                    "framework_revision": 1,
                    "framework_diff_hash": None,
                    "source_revisions": draft["draft_claim_set"]["source_revisions"],
                    "claim_results": [
                        {
                            "claim_id": draft["draft_claim_set"]["claims"][0]["claim_id"],
                            "result": "direct",
                            "evidence_unit_ids": draft["draft_claim_set"]["claims"][0][
                                "evidence_unit_ids"
                            ],
                            "auditor_note": "",
                            "propagated_caveat_ids": [],
                        }
                    ],
                    "audit_status": "passed",
                    "created_at": "2026-09-04T00:00:00Z",
                }
            }
            receipt_path = write_json(directory, "receipt.json", receipt)
            passing = run_script(
                "validate_claim_audit.py", str(draft_path), "--receipt", str(receipt_path)
            )
            self.assertEqual(passing.returncode, 0, passing.stderr)
            draft["draft_claim_set"]["claims"][0]["exact_text"] = "A changed claim."
            drift_path = write_json(directory, "drift.json", draft)
            drift = run_script(
                "validate_claim_audit.py", str(drift_path), "--receipt", str(receipt_path)
            )
        self.assertEqual(drift.returncode, 1)
        self.assertIn("does not match", drift.stderr)

    def test_receipt_rejects_substituted_evidence_unit(self) -> None:
        draft = self.build_draft()
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            draft_path = write_json(directory, "draft.json", draft)
            digest_result = run_script("validate_claim_audit.py", str(draft_path))
            self.assertEqual(digest_result.returncode, 0, digest_result.stderr)
            digest = json.loads(digest_result.stdout)["audited_draft_hash"]
            draft["draft_claim_set"]["audited_draft_hash"] = digest
            draft_path = write_json(directory, "draft.json", draft)
            claim = draft["draft_claim_set"]["claims"][0]
            receipt = {
                "claim_audit_receipt": {
                    "draft_claim_set_id": draft["draft_claim_set"]["draft_claim_set_id"],
                    "audited_draft_hash": digest,
                    "evidence_pack_id": draft["draft_claim_set"]["evidence_pack_id"],
                    "evidence_pack_checksum": draft["draft_claim_set"][
                        "evidence_pack_checksum"
                    ],
                    "framework_revision": 1,
                    "framework_diff_hash": None,
                    "source_revisions": draft["draft_claim_set"]["source_revisions"],
                    "claim_results": [
                        {
                            "claim_id": claim["claim_id"],
                            "result": "direct",
                            "evidence_unit_ids": [
                                "evu_01991d8e-1234-7abc-8def-c234567890ab"
                            ],
                            "propagated_caveat_ids": [],
                        }
                    ],
                    "audit_status": "passed",
                }
            }
            receipt_path = write_json(directory, "receipt.json", receipt)
            result = run_script(
                "validate_claim_audit.py", str(draft_path), "--receipt", str(receipt_path)
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("evidence_unit_ids do not match", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_partial_receipt_requires_concrete_propagated_caveat(self) -> None:
        draft = self.build_draft()
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            draft_path = write_json(directory, "draft.json", draft)
            digest_result = run_script("validate_claim_audit.py", str(draft_path))
            self.assertEqual(digest_result.returncode, 0, digest_result.stderr)
            digest = json.loads(digest_result.stdout)["audited_draft_hash"]
            draft["draft_claim_set"]["audited_draft_hash"] = digest
            draft_path = write_json(directory, "draft.json", draft)
            claim = draft["draft_claim_set"]["claims"][0]
            receipt = {
                "claim_audit_receipt": {
                    "draft_claim_set_id": draft["draft_claim_set"]["draft_claim_set_id"],
                    "audited_draft_hash": digest,
                    "evidence_pack_id": draft["draft_claim_set"]["evidence_pack_id"],
                    "evidence_pack_checksum": draft["draft_claim_set"][
                        "evidence_pack_checksum"
                    ],
                    "framework_revision": 1,
                    "framework_diff_hash": None,
                    "source_revisions": draft["draft_claim_set"]["source_revisions"],
                    "claim_results": [
                        {
                            "claim_id": claim["claim_id"],
                            "result": "partial",
                            "evidence_unit_ids": claim["evidence_unit_ids"],
                            "propagated_caveat_ids": [],
                        }
                    ],
                    "audit_status": "passed_with_caveat",
                }
            }
            receipt_path = write_json(directory, "receipt.json", receipt)
            result = run_script(
                "validate_claim_audit.py", str(draft_path), "--receipt", str(receipt_path)
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires propagated caveat IDs", result.stderr)
        self.assertIn("requires at least one propagated caveat ID", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


class DomainSkillScoreTests(unittest.TestCase):
    def test_hard_failure_excludes_high_scoring_candidate(self) -> None:
        result = run_script(
            "score_domain_skill.py", str(FIXTURES / "domain-candidates.json")
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(
            [candidate["candidate_id"] for candidate in payload["eligible_candidates"]],
            ["dsc_01991d8e-1234-7abc-8def-b234567890ab"],
        )

    def test_non_object_candidate_fails_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(
                Path(temporary),
                "invalid-candidates.json",
                {"domain_skill_candidate_manifest": {"candidates": [1]}},
            )
            result = run_script("score_domain_skill.py", str(path))
        self.assertEqual(result.returncode, 2)
        self.assertIn("candidate must be an object", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_candidate_ids_fail(self) -> None:
        payload = json.loads(
            (FIXTURES / "domain-candidates.json").read_text(encoding="utf-8")
        )
        candidates = payload["domain_skill_candidate_manifest"]["candidates"]
        candidates[1]["candidate_id"] = candidates[0]["candidate_id"]
        candidates[1]["vetoes"] = []
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(Path(temporary), "duplicate-candidates.json", payload)
            result = run_script("score_domain_skill.py", str(path))
        self.assertEqual(result.returncode, 2)
        self.assertIn("must be unique", result.stderr)

    def test_candidate_display_limit_cannot_exceed_three(self) -> None:
        result = run_script(
            "score_domain_skill.py",
            str(FIXTURES / "domain-candidates.json"),
            "--limit",
            "4",
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("between 1 and 3", result.stderr)

    def test_missing_source_provenance_rejects_candidate_manifest(self) -> None:
        payload = json.loads(
            (FIXTURES / "domain-candidates.json").read_text(encoding="utf-8")
        )
        del payload["domain_skill_candidate_manifest"]["candidates"][0]["source"][
            "resolved_commit"
        ]
        with tempfile.TemporaryDirectory() as temporary:
            path = write_json(Path(temporary), "missing-provenance.json", payload)
            result = run_script("score_domain_skill.py", str(path))
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing source provenance fields: resolved_commit", result.stderr)
        self.assertNotIn("Traceback", result.stderr)


class DomainSkillNameTests(unittest.TestCase):
    def base_arguments(self) -> list[str]:
        return [
            "--project-slug",
            "bridge-audit",
            "--field-slug",
            "engineering-standards",
            "--upstream-slug",
            "eurocode-assistant",
            "--project-display",
            "Bridge Audit",
            "--field-display",
            "Engineering Standards",
            "--upstream-display",
            "Eurocode Assistant",
            "--source-identity",
            "owner/repo:skills/eurocode@012345",
            "--source-label",
            "owner/repo@01234567",
        ]

    def test_expected_names_are_generated(self) -> None:
        result = run_script("generate_domain_skill_name.py", *self.base_arguments())
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(
            payload["display_name"],
            "[Bridge Audit]-[Engineering Standards] Eurocode Assistant",
        )
        self.assertLessEqual(len(payload["canonical_name"]), 64)
        self.assertEqual(
            payload["default_prompt_skill_token"], f"${payload['canonical_name']}"
        )
        self.assertEqual(
            payload["short_description"], "GitHub Skill: owner/repo@01234567"
        )

    def test_long_name_is_deterministically_hash_suffixed(self) -> None:
        arguments = self.base_arguments()
        arguments[1] = "extremely-long-project-identity-for-a-regulated-bridge-program"
        first = run_script("generate_domain_skill_name.py", *arguments)
        second = run_script("generate_domain_skill_name.py", *arguments)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)
        canonical = json.loads(first.stdout)["canonical_name"]
        self.assertLessEqual(len(canonical), 64)
        self.assertIn("engineering", canonical)
        self.assertIn("eurocode", canonical)
        self.assertRegex(canonical, r"-[0-9a-f]{8}$")

    def test_ambiguous_display_brackets_are_rejected(self) -> None:
        arguments = self.base_arguments()
        arguments[9] = "[Engineering] Standards"
        result = run_script("generate_domain_skill_name.py", *arguments)
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot contain square brackets", result.stderr)

    def test_non_english_display_alias_is_rejected(self) -> None:
        arguments = self.base_arguments()
        arguments[9] = "Field " + chr(0x5DE5)
        result = run_script("generate_domain_skill_name.py", *arguments)
        self.assertEqual(result.returncode, 2)
        self.assertIn("English ASCII alias", result.stderr)


if __name__ == "__main__":
    unittest.main()
