# Claim and Evidence Contract

This contract keeps formal publication claims traceable without turning evidence control into a user-facing bureaucracy.

## Principle

Zotero establishes what evidence is available and what it can support. Notion Author owns the exact publication wording. Zotero Source Gate audits that wording internally before publication. The user reviews the finished publication, not an evidence schema or claim-audit receipt.

## Evidence Model

An admitted source contains one or more locator-specific EvidenceUnits. Each unit records internally:

- source and Zotero item identity;
- exact version, date, jurisdiction, or commit when relevant;
- page, section, timestamp, paragraph, file, line, table, or other stable locator;
- the support scope and important caveats;
- a content fingerprint;
- accessibility and conflict status.

An EvidenceUnit must identify one inspectable source object through a stable source, Zotero, DOI, ISBN, URL, or commit identity and one structured stable locator. A title-only object is not source identity. The locator records a permitted kind and exact value for a page, page range, section, subsection, paragraph, timestamp, time range, line range, table, figure, equation, or record. A section or subsection locator also requires a bounded internal anchor; `chapter`, `document`, `collection`, whole-section placeholders without an anchor, and source-pack-level locators are not precise enough. Each unit also lists the exact `supported_claim_ids` and a SHA-256 content fingerprint. A chapter-wide label such as "relevant admitted sources," a source-pack reference without source identity, or a generic statement that all inline citations are adequate is not an EvidenceUnit. Reusing one unit across several claims is allowed only when its locator and declared support scope directly cover each listed exact claim.

An EvidencePack is an immutable set of EvidenceUnits assembled for a framework or publication revision. Its checksum is recomputed from JCS-style canonical content while excluding the checksum field itself; copying an earlier checksum onto changed locators or support scopes is invalid. It is machine state, not a reading list shown for approval.

## Claim Intent

Framework creates ClaimIntents describing what a chapter or concept needs to establish. A ClaimIntent is a sourcing target, not a factual assertion. It may identify the desired support level, relevant source types, and unresolved evidence gaps.

## Draft Claims

Notion Author first completes the substantive publication draft for the current audited publication unit and routes that whole unit through `notion-natural-prose-editor`. A focused work may have one unit; a large coverage-first publication may have many framework-bound units tracked by the PublicationCoverageIndex. After the edited unit returns and the author accepts or corrects its changes, Notion Author extracts every fact-bearing statement in that unit into the final internal DraftClaimSet. Each claim records its exact text, target section, supporting EvidenceUnits, and required support. Explanatory transitions or clearly marked original synthesis may be classified as non-claim content, but the classification must not be used to hide factual assertions.

The canonical hash covers the entire fact-bearing draft. A meaningful wording change invalidates the previous audit.

## Audit Results

Zotero Source Gate classifies each claim as:

- `direct`: the cited evidence supports the exact statement;
- `partial`: only a properly qualified portion is supported;
- `contradictory`: admitted evidence materially conflicts with the statement;
- `unsupported`: no admitted evidence supports the statement at the required scope.

Only a complete DraftClaimSet whose claims are direct or properly caveated partial claims may receive a passing ClaimAuditReceipt. Contradictory or unsupported wording returns to Notion Author for revision, removal, or additional sourcing.

Each claim result records a concise `support_assessment` explaining how the cited locator supports the exact statement. Matching IDs, a citation number, or the presence of an EvidencePack does not establish semantic support. The audit owner must inspect the claim and locator; a deterministic script may validate bindings and completeness but may not generate a passing semantic result.

The receipt binds the draft hash, EvidencePack checksum, source revisions, framework revision, claim IDs, results, and propagated caveats. It is stored internally and never inserted into Notion or presented as a routine user gate.

## Citation Handoff

For every distinct source used by a passing claim, Zotero Source Gate returns citation-ready metadata alongside the internal receipt. Notion Author uses that metadata, the exact DraftClaimSet, and the EvidencePack to create the reader-facing CitationProjection. Source identity and locator remain internal; only publication numbers, formatted references, and original links appear in Notion.

The factual claim audit remains bound to the fact-bearing draft. CitationProjection records both that source hash and the projected reader-facing hash. A deterministic projection validator checks citation closure and source bindings before publication; it does not decide whether claims are supported and does not replace this audit.

## Product Outputs

A product task that makes material external claims, relies on a standard, or depends on factual compatibility or safety constraints must use admitted evidence appropriate to those claims. A purely local implementation or transformation may proceed without manufacturing a formal evidence-exemption receipt. The task owner records why external evidence is or is not applicable in machine state.

## Invalidation

Re-audit when any of the following changes materially:

- factual wording or qualification;
- cited source or locator;
- source version, date, jurisdiction, or retraction state;
- EvidencePack checksum;
- the framework relationship that changes the claim's meaning.

Formatting, heading wording, citation-number renumbering, or a URL label change does not require a new audit when factual meaning and support remain identical. A prose edit performed after an audit may reuse the receipt only when canonicalization proves that the fact-bearing draft is unchanged; otherwise route the revision back through claim audit.

## Prohibitions

- Do not treat source selection as proof that every drafted statement is supported.
- Do not approve a topic summary in place of the exact publication wording.
- Do not use a search snippet, AI summary, citation metadata, or inaccessible full text beyond what it directly supports.
- Do not create one generic chapter-level EvidenceUnit and bind it mechanically to every claim.
- Do not mark claims `direct` from identifier equality, citation presence, title counts, character counts, or hard-coded passing results.
- Do not ask the user to inspect DraftClaimSets, EvidencePacks, hashes, or receipts unless they explicitly request an audit diagnostic.
- Do not create source-preview or manual-embed tasks; References use ordinary clickable links only.
