---
name: notion-node-author
description: Write, revise, and publish formal reader-facing Notion textbook chapters, including bounded DraftPackets in a large publication, or explicitly requested product documents from an approved framework and Zotero-admitted evidence. Use for canonical publication prose, natural headings, relationships, citations, and references; do not run post-write content audits or use Notion for questions, status, schemas, previews, or workflow chatter.
---

# Notion Textbook Author

Make Notion read like a finished work written for a person. For knowledge projects, author a coherent textbook or monograph. For product projects, publish only a requested final manual, specification, decision document, or report.

## Required Contracts

Read [workflow-contracts.md](../../references/workflow-contracts.md) before handoff. Read [large-publication-state-contract.md](../../references/large-publication-state-contract.md) before authoring, repairing, or publishing any `large_publication` unit. Read [notion-node-template.md](../../references/notion-node-template.md) for the adaptive editorial model. Read [curriculum-coverage-policy.md](../../references/curriculum-coverage-policy.md) before authoring a textbook, curriculum, comprehensive survey, or other coverage-first publication. Read [managed-content-boundaries.md](../../references/managed-content-boundaries.md) before any write. Read [claim-evidence-contract.md](../../references/claim-evidence-contract.md) and [citation-and-embed-policy.md](../../references/citation-and-embed-policy.md) before drafting claims or References.

Use [Notion Natural Prose Editor](../notion-natural-prose-editor/SKILL.md) only when the user explicitly requests polishing or concrete prose feedback shows that a bounded revision is needed. It is not a default pass. Notion Author remains the sole owner of factual wording, Zotero claim-audit requests, and publication.

## Inputs

Require current ProjectContext, Notion publication binding, GoalContract, FrameworkSpec, relevant nodes and relations, admitted EvidencePack, and any approved reuse or evolution lineage. For coverage-first work, also require the current CoverageContract, TopicCoverageMatrix, OmissionLedger, and CoverageAuditReceipt. Refuse a stale or non-passing coverage receipt.

For `large_publication` work, additionally require the canonical `FullBookChapterKnowledgeMap`, current queued DraftPacket with a successful `packet-dispatch` gate, its dispatch ID and capacity reservation, complete local knowledge obligations, adjacent accepted prose or continuity capsule, and the external checkpoint binding supplied by the orchestrator. Refuse a Packet bound to stale requirement, map, framework, evidence, body, or publication revisions. Never start from a chapter title alone or author a second Packet under the same dispatch or execution ID.

## Authoring

1. Choose a natural editorial structure suited to the subject, audience, and genre.
2. Write complete explanations with appropriate definitions, reasoning, mechanisms, formulas, examples, limitations, applications, and transitions.
3. Use nested pages when they improve conceptual hierarchy; make parent and child pages useful to readers.
4. Integrate relationship and combination content in the most relevant chapter. Use ordinary prose, subsections, tables, examples, or toggles; a link alone is not enough.
5. Use natural titles and headings. Never expose Stable ID, Base Capsule, Core Content, Verification, Relation ID, Combination ID, audit state, or other machine labels.
6. Place numbered citations close to supported claims and finish with clean formatted References and clickable original URLs. Keep broader uncited structural sources under `Recommended Reading`, never under References.
7. Never add Source View images, screenshots, thumbnails, bookmark previews, iframes, HTML embeds, or expanded source cards.
8. Express all mathematics as LaTeX: `$...$` inline and `$$...$$` in display blocks in the source draft. Never use backticks or Unicode math operators as formula substitutes. Publish with native Notion equation blocks when the connector supports them; do not fetch the page afterward solely to audit rendering.
9. Default to direct, plain-language explanation for a competent reader. When definitions, mechanisms, derivations, and consequences make the subject clear, do not add a case merely to make the presentation appear accessible.
10. For unfamiliar, highly abstract, cross-layer, or counterintuitive domains, use a running case when it materially reduces the reader's reconstruction burden. Map the case explicitly to the modeled problem, variables, assumptions, inference target, objective, update or action, consequence, and validity boundary. The case is an explanatory scaffold, not a substitute for the theory, and its analogy limits must remain visible.
11. Treat Framework nodes and DraftPackets as hidden production structure. Several related nodes and several Packets may become one continuous reader-facing teaching topic. Create a heading only when the reader encounters a real change of problem, object, or reasoning stage.
12. For most core explanatory paragraphs, identify the concept, explain how or why it works, and connect it to its consequence, use, prerequisite, contrast, or next idea. This is flexible paragraph logic, not a fixed visible template.

## Large Publication Units

For a publication too large for one reliable drafting pass, preserve the current global hierarchy and canonical chapter-to-knowledge map, then author the orchestrator-scheduled DraftPackets in dependency order. A DraftPacket is a hidden reliable generation and recovery unit, not a page or heading. Do not compress, merge away, or omit mapped knowledge to fit a context window or connector operation; return `needs_split` when the complete local obligations cannot fit with adequate output capacity.

Maintain a lightweight PublicationCoverageIndex that assigns each included framework target and substantive knowledge point to its teaching topic, DraftPacket, and intended published page. Populate it during scheduling and writing. For a coherent large-publication unit, provide the canonical local draft once for the Architect's bounded pre-publication DraftQualityReview; do not perform a second review or any post-write prose-location audit. Bind each Packet to the current requirement, map, framework, coverage, evidence, body, review, and publication revisions. A later Packet may rely on earlier accepted prose, but a link or title does not replace the explanation allocated to the current obligations.

Draft only the current Packet from its complete obligations, local evidence, terminology and notation, adjacent accepted prose, and next-step intent. One Author invocation produces one Packet draft. If the complete obligations cannot be explained within the reserved output capacity, return `needs_split` before drafting instead of shortening them. Never load the complete book merely to make one local passage sound consistent. Return the exact draft content reference, content SHA-256, execution ID, and completion time so the orchestrator can persist a checkpoint and pass `packet-checkpoint`. A dependent Packet must not start before that checkpoint is accepted. After runtime compaction or restart, recover accepted text from the checkpoint rather than model memory. A compaction summary cannot mark work accepted or replace accepted prose.

Assemble accepted Packets in canonical order. Reconcile only adjacent seams, duplicated setup, terminology, and transitions while writing; never request a global summarizing rewrite of a large chapter or book. A later factual edit invalidates its Zotero claim audit and must return only to that source-audit step before republishing.

Return to the orchestrator when a unit exposes a missing prerequisite, an uncovered baseline topic, or a scope conflict. Do not repair the CoverageContract or OmissionLedger as the author.

## Single Draft Review, Zotero Audit, and Direct Publication

Draft the complete fact-bearing payload for the current reliable authoring unit and apply the natural prose editor only under its explicit trigger. For `large_publication` work, assemble only accepted Packet hashes, persist the canonical unit hash, and return it to the orchestrator for exactly one Architect DraftQualityReview before claim extraction. Do not author the review or invoke a script to certify your own draft. Address each substantive finding once with one distinct bounded repair execution, or mark the affected obligation as needing its real evidence/scope owner. Record one terminal disposition per finding and the resulting final draft hash; do not request an Architect re-review of the repaired draft.

After the `claim-audit-ready` gate, extract every exact fact-bearing statement from the final canonical draft into the internal DraftClaimSet and return one claim-audit request plus the exact immutable EvidencePack through the orchestrator to `zotero-source-gate`. Each claim must name locator-specific EvidenceUnits; a generic chapter EvidenceUnit or source-pack reference is invalid. Revise only claims the Zotero audit identifies as unsupported, contradictory, or insufficiently qualified; any later factual wording change requires a fresh Zotero claim audit but not another Architect review in the same publication run.

When the claim audit passes, create one `CitationProjection` from the exact audited DraftClaimSet, EvidencePack, and citation-ready Zotero metadata. Assign one contiguous number per distinct source in first-use order, replace all internal authoring placeholders with numbered aliases, and generate a References section from the same manifest. Never expose Zotero keys, source IDs, EvidenceUnit IDs, claim IDs, locators, or debug labels. Preserve the audited fact-draft hash as `source_draft_sha256` and record the rendered reader-facing draft as `projected_draft_sha256`; citation projection may not alter factual wording. Run [validate_citation_projection.py](../../scripts/validate_citation_projection.py) with `--source-draft` plus the projected draft, manifest, exact DraftClaimSet, and EvidencePack. A failure blocks `publish-ready` and returns only to citation projection unless factual wording changed.

Publish only after the orchestrator passes `publish-ready` for a passing CitationProjection whose source hash is the exact audited fact draft. Publish the projected reader-facing draft and bind the operation to its projected hash. Treat a successful connector response containing the expected native page identity or URL as the publication result; record the operation ID, returned target identity, projected draft hash, and time, but do not reload, reread, semantically inspect, count blocks, or audit equations, citations, hierarchy, and references after writing. A connector error or missing target identity is a write failure, not a reason to launch a content audit. Do not ask for TemplateProfile approval, a page preview, per-block approval, or a technical mutation preview. The actual Notion publication is the user review surface.

## Absolute Exclusions

Never place these in Notion:

- questions to the user or their answers;
- source shortlists, candidate manifests, audits, receipts, hashes, validation output, or debug data;
- goals, project status, task queues, checkpoints, decisions, or review requests;
- internal YAML, JSON, schema terminology, connector data, or execution commentary.

Do not create a manual task when a source preview cannot be embedded; previews are prohibited and a normal link is the correct output.

## Revision and Safety

Preserve user-authored blocks and write only to internally identifiable managed pages or regions. Ordinary reversible writes within the confirmed publication root proceed under scoped authorization. Escalate ambiguous identity, overwrite conflict, deletion, out-of-scope movement, or material risk.

Return the DraftQualityReview finding dispositions when applicable, DraftClaimSet, ClaimAuditRequest, CitationProjection, the lightweight PublicationCoverageIndex, Packet checkpoint facts, and NotionPublicationPack with connector-returned page identities to `knowledge-product-orchestrator`. The orchestrator owns the DraftPacket queue, checkpoint aggregation, and full-book completion barrier. Do not create Notion audit receipts or reread the publication for internal acceptance. User-facing reporting should link to the actual publication and invite content feedback in natural language. Never report a book complete because only one Packet, chapter, or part was published.
