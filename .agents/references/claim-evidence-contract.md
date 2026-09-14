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

An EvidencePack is an immutable set of EvidenceUnits assembled for a framework or publication revision. It is machine state, not a reading list shown for approval.

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

The receipt binds the draft hash, EvidencePack checksum, source revisions, framework revision, claim IDs, results, and propagated caveats. It is stored internally and never inserted into Notion or presented as a routine user gate.

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
- Do not ask the user to inspect DraftClaimSets, EvidencePacks, hashes, or receipts unless they explicitly request an audit diagnostic.
- Do not create source-preview or manual-embed tasks; References use ordinary clickable links only.
