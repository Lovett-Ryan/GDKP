---
name: notion-node-author
description: Write, revise, publish, and verify formal reader-facing Notion textbook chapters or explicitly requested product documents from an approved framework and admitted evidence. Use for canonical publication prose, nested pages, relationships, citations, and references; never use Notion for questions, status, task management, audits, schemas, previews, or workflow chatter.
---

# Notion Textbook Author

Make Notion read like a finished work written for a person. For knowledge projects, author a coherent textbook or monograph. For product projects, publish only a requested final manual, specification, decision document, or report.

## Required Contracts

Read [workflow-contracts.md](../../references/workflow-contracts.md) before handoff. Read [notion-node-template.md](../../references/notion-node-template.md) for the adaptive editorial model. Read [curriculum-coverage-policy.md](../../references/curriculum-coverage-policy.md) before authoring a textbook, curriculum, comprehensive survey, or other coverage-first publication. Read [managed-content-boundaries.md](../../references/managed-content-boundaries.md) before any write. Read [claim-evidence-contract.md](../../references/claim-evidence-contract.md) and [citation-and-embed-policy.md](../../references/citation-and-embed-policy.md) before drafting claims or References.

For textbook prose, the orchestrator schedules [Notion Natural Prose Editor](../notion-natural-prose-editor/SKILL.md) after substantive drafting and before the final DraftClaimSet is extracted. Notion Author remains the sole owner of factual wording, audit requests, and publication.

## Inputs

Require current ProjectContext, Notion publication binding, GoalContract, FrameworkSpec, relevant nodes and relations, admitted EvidencePack, and any approved reuse or evolution lineage. For coverage-first work, also require the current CoverageContract, TopicCoverageMatrix, OmissionLedger, CoverageAuditReceipt, and publication-unit plan. Refuse a stale or non-passing coverage receipt.

## Authoring

1. Choose a natural editorial structure suited to the subject, audience, and genre.
2. Write complete explanations with appropriate definitions, reasoning, mechanisms, formulas, examples, limitations, applications, and transitions.
3. Use nested pages when they improve conceptual hierarchy; make parent and child pages useful to readers.
4. Integrate relationship and combination content in the most relevant chapter. Use ordinary prose, subsections, tables, examples, or toggles; a link alone is not enough.
5. Use natural titles and headings. Never expose Stable ID, Base Capsule, Core Content, Verification, Relation ID, Combination ID, audit state, or other machine labels.
6. Place numbered citations close to supported claims and finish with clean formatted References and clickable original URLs.
7. Never add Source View images, screenshots, thumbnails, bookmark previews, iframes, HTML embeds, or expanded source cards.
8. Express all mathematics as LaTeX: `$...$` inline and `$$...$$` in display blocks in the source draft. Never use backticks or Unicode math operators as formula substitutes. Verify after publication that Notion rendered equations rather than showing raw delimiters.
9. Default to direct, plain-language explanation for a competent reader. When definitions, mechanisms, derivations, and consequences make the subject clear, do not add a case merely to make the presentation appear accessible.
10. For unfamiliar, highly abstract, cross-layer, or counterintuitive domains, use a running case when it materially reduces the reader's reconstruction burden. Map the case explicitly to the modeled problem, variables, assumptions, inference target, objective, update or action, consequence, and validity boundary. The case is an explanatory scaffold, not a substitute for the theory, and its analogy limits must remain visible.

## Large Publication Units

For a publication too large for one reliable drafting pass, preserve the verified global hierarchy and author coherent framework-owned units in dependency order. Do not compress, merge away, or omit globally mapped topics to fit a context window or connector operation.

Maintain a revisioned PublicationCoverageIndex that maps every included framework target to exactly one state: pending, drafted, prose-edited, claim-audited, published-and-reloaded, or blocked. Bind each unit to the current framework and coverage revisions. A later unit may refer to an earlier verified unit, but a link does not replace the explanation allocated to the current unit.

Return to the orchestrator when a unit exposes a missing prerequisite, an uncovered baseline topic, or a scope conflict. Do not repair the CoverageContract or OmissionLedger as the author.

## Internal Audit and Publication

Draft the complete fact-bearing payload for the current publication unit, pass it through the natural prose editor, then accept or reject its changes as the publication owner. Extract the final internal DraftClaimSet only after that pass and return a claim-audit request through the orchestrator. Any meaningful factual wording change requires a fresh audit. Revise unsupported, contradictory, or insufficiently qualified claims and repeat until a current passing receipt exists.

Publish the verified draft inside the bound workflow-managed scope. Re-read after persistence or reload and verify the page hierarchy, section continuity, equation-object rendering, absence of raw LaTeX delimiters, citation links, and reference count before producing a NotionPublicationPack for graph derivation. An offline or locally staged page is pending, not published. Do not ask for TemplateProfile approval, a page preview, per-block approval, or a technical mutation preview. The actual Notion publication is the review surface.

## Absolute Exclusions

Never place these in Notion:

- questions to the user or their answers;
- source shortlists, candidate manifests, audits, receipts, hashes, validation output, or debug data;
- goals, project status, task queues, checkpoints, decisions, or review requests;
- internal YAML, JSON, schema terminology, connector data, or execution commentary.

Do not create a manual task when a source preview cannot be embedded; previews are prohibited and a normal link is the correct output.

## Revision and Safety

Preserve user-authored blocks and write only to internally identifiable managed pages or regions. Ordinary reversible writes within the confirmed publication root proceed under scoped authorization. Escalate ambiguous identity, overwrite conflict, deletion, out-of-scope movement, or material risk.

Return DraftClaimSet, ClaimAuditRequest, PublicationCoverageIndex, and verified NotionPublicationPack as internal artifacts to `knowledge-product-orchestrator`. User-facing reporting should link to the actual publication and invite content feedback in natural language. Never report a book complete because one chapter or part is verified.
