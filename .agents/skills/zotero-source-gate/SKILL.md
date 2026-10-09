---
name: zotero-source-gate
description: Register, normalize, discover, audit, and admit structural curriculum sources and factual project evidence through Zotero, then audit exact publication claims. Use for broad-domain coverage baselines, user sources, supplemental shortlists, evidence gaps, source revisions, or factual draft audits; do not write publication prose or graph notes.
---

# Zotero Source Gate

Make Zotero the evidence gate for formal knowledge and externally grounded product claims without burdening the user with library mechanics.

## Required Contracts

Read [workflow-contracts.md](../../references/workflow-contracts.md) before handoff. Read [large-publication-state-contract.md](../../references/large-publication-state-contract.md) for a `large_publication` claim audit. Read [curriculum-coverage-policy.md](../../references/curriculum-coverage-policy.md) before structural-source work. Read [zotero-item-normalization.md](../../references/zotero-item-normalization.md) before matching or writing items. Read [claim-evidence-contract.md](../../references/claim-evidence-contract.md) before evidence or claim auditing. Read [question-gates.md](../../references/question-gates.md) before a supplemental shortlist. Read [citation-and-embed-policy.md](../../references/citation-and-embed-policy.md) for citation-ready output.

## Preconditions

Require current ProjectContext, SourcePolicy, Zotero binding, and the relevant user sources, candidates, CoverageProfile, ClaimIntents, or DraftClaimSet. The default binding is one root-level `GDKP-<Project Name>` collection with no automatic subcollections.

For coverage-first structural discovery, IntentContract, CoverageProfile, ScopeDecisionLedger, and SourcePolicy are sufficient inputs before requirement reconstruction. If Zotero cannot be written, an exact user-specified or user-approved local document may support a `local_files_verified` CoverageBaseline only after location, content digest, extraction method, read-back, and authorization are verified. This degraded baseline is not Zotero admission or factual evidence.

## Structural Coverage Baseline

When `coverage_first` applies:

1. Register user-specified structural sources acknowledged during intake without another question.
2. Discover AI-suggested structural sources only inside the SourcePolicy, then use the ordinary one-time supplemental shortlist decision before admission.
3. Prefer authoritative textbook tables of contents, recognized syllabi or competency frameworks, and high-quality surveys or taxonomies. Use independent sources where one tradition, application, or publication date could create a blind spot.
4. Extract natural topic names, aliases, hierarchy, prominence, dependencies, source membership, disagreements, scope limits, and freshness into a revisioned CoverageBaseline.
5. Separate structural role from factual-evidence role. A table of contents can establish that a topic belongs in the map; it cannot support the chapter's factual claims.
6. Expose baseline blind spots and unresolved source disagreement. Do not collapse minority but material branches solely because they appear in fewer sources.
7. Return the verified CoverageBaseline to the orchestrator for requirement reconstruction and framework design. Do not create Containers, depth assignments, or publication prose.

When the verified input is a local document rather than a Zotero-admitted item, set the baseline and source status to `local_files_verified`. Record `location_ref`, `content_sha256`, `extraction_method`, `readback_verified: true`, and an explicit user authorization reference. Permit downstream framework work to report only `coverage_local_verified`. Retry normal Zotero admission before factual claim audit or citation use.

## Source Admission

1. Register user-specified sources acknowledged during intake without another source-selection question.
2. Discover supplements only within the approved policy and only when they fill a real coverage or quality gap.
3. For AI-suggested additions, show one concise Codex shortlist with title, type or publisher, purpose, and material limitation. Ask once for all, a subset, or none.
4. After authorization, import or link the batch, normalize metadata, deduplicate, attach project collection membership, re-read, and verify without item-by-item previews.
5. Ask only for ambiguous merges, out-of-policy sources, paid or inaccessible content, overwrite of user-curated metadata, destructive change, or material risk.
6. Audit authority, relevance, currency, version, jurisdiction, independence, accessibility, conflicts, and locator precision.
7. Admit only content capable of supporting the intended claim at the required locator granularity.

Coverage gaps include missing canonical topics identified by structural comparison, not only ClaimIntents already emitted by a framework.

A search snippet or AI summary is never evidence. Preserve user priority separately from evidence quality, and never silently replace a user-primary source.

## Claim Audit

Audit the complete exact DraftClaimSet against its immutable EvidencePack in a dedicated source-gate execution. Resolve every EvidenceUnit to a concrete source or Zotero item identity, structured passage/table/figure/equation locator, exact supported claim IDs, support scope, content fingerprint, accessibility state, and conflict status. Recompute the EvidencePack checksum from canonical content. Inspect the exact claim against those locators and record a concise `support_assessment`; matching IDs, citation presence, or a chapter-level source summary cannot establish support. Classify claims as direct, partial, contradictory, or unsupported. A partial claim passes only when the published wording carries the necessary qualification. Return unsupported or contradictory wording to Notion Author through the orchestrator.

Bind a passing ClaimAuditReceipt to the draft hash, source and evidence revisions, claim IDs, exact EvidenceUnit IDs, support assessments, and caveats. Before returning a passing receipt, run [validate_claim_audit.py](../../scripts/validate_claim_audit.py) with `--receipt` and the exact `--evidence-pack`. The script validates structure and bindings only; it never generates claim results or substitutes for source inspection. For every distinct source used by a passing claim, also return citation-ready Zotero metadata to Notion Author: concrete source identity, item type, creators, title, container or publisher, year, edition or version, volume, issue, pages, DOI, and original URL when available. Omit unknown fields rather than inventing them. Keep the EvidencePack, DraftClaimSet, citation-source metadata, audit detail, hashes, and receipt internal. Do not ask the user to approve them.

## Product Evidence

Support product tasks when their standards, recommendations, compatibility, safety conditions, or other external claims require evidence. Purely local transformations may proceed without creating an evidence-exemption receipt.

## Boundaries and Output

- Write only inside the bound collection and workflow-owned metadata scope.
- Do not reorganize unrelated Zotero library content.
- Do not create Notion Source Views or reference previews.
- Do not fabricate authors, identifiers, locators, versions, or inaccessible content.
- Do not write publication prose, relations, or graph notes.
- Do not represent an inspected or merely proposed structural source as an admitted CoverageBaseline. The `local_files_verified` exception requires an exact authorized file plus identity, digest, extraction, and read-back verification.
- Do not treat structural prominence as proof of a factual claim.

Internally produce CandidateManifest when needed, CoverageBaseline for coverage-first work, source decision record, verified Zotero operations, SourceAuditReport, EvidencePack, ClaimAuditReceipt, and a citation-ready source set for the passing claims. Return them to `knowledge-product-orchestrator`; the user sees only the supplemental shortlist, a readable framework decision, or a material source problem.
