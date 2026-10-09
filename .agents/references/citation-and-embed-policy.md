# Citation and Link Policy

This policy governs citations in Notion publications and derived Obsidian notes.

## Source of Truth

Every factual publication claim must trace to an admitted Zotero source and locator. Zotero item keys and internal source IDs provide machine identity; visible numbering is a publication alias.

Never cite a search result snippet, AI answer, unverified summary, or inaccessible metadata record as if it supported the claim.

## In-Text Citations

Use numbered citations such as `[1]` close to the supported statement. Reuse the same number for the same source within a publication scope. Cite at the granularity needed to distinguish competing, versioned, jurisdiction-specific, or qualified claims.

Zotero item keys, EvidenceUnit IDs, locators, claim IDs, and authoring placeholders are internal identities. They may exist in an unpublished working draft or machine artifact, but they must never appear in the reader-facing publication draft.

## Citation Projection

After the final factual wording passes the Zotero claim audit, Notion Author creates one deterministic `CitationProjection` for that exact publication unit. The projection maps every audited source identity used by the DraftClaimSet to:

- one contiguous publication number assigned in first-use order;
- the exact claim IDs supported by that source;
- a formatted reader-facing reference;
- the original HTTP(S) URL or stable locator when Zotero has one.

Apply the projection without changing factual wording. Replace internal citation placeholders with numbered aliases, generate the numbered References section from the same entries, and preserve the audited fact-draft hash separately from the projected publication-draft hash. A citation-number, link-label, or bibliography-format change invalidates the projection and pending publication, but not the factual claim audit when the fact-bearing text is unchanged.

Before `publish-ready`, run [validate_citation_projection.py](../scripts/validate_citation_projection.py) against the source fact draft, projected draft, and manifest. For formal factual content, also pass the exact DraftClaimSet and EvidencePack. The validator must reject a source-hash mismatch, internal source identifiers, missing or orphaned numbers, duplicate source aliases, bibliography drift, missing clickable URLs declared by the projection, and a projection whose source-to-claim bindings differ from the audited evidence.

## Reference Formatting

### Papers and formal publications

Use IEEE reference style with available authors, title, venue or publisher, year, volume, issue, pages, DOI, standard number, or edition as applicable. Do not fabricate missing fields.

### Webpages and online resources

Use the exact page or site title, publisher or organization when known, version or publication date when relevant, and access date when volatility matters.

### Courses, videos, repositories, datasets, records, and private material

Use a natural title plus creator or organization, version or date, and the most precise stable locator available. Mark access restrictions or private provenance when needed.

## URL Presentation

Every reference should provide a directly clickable original URL or stable locator when one exists. Use a normal text link only.

Never add any of the following to a References section:

- Source View images;
- screenshots or page captures;
- thumbnails or cover previews;
- Notion bookmark previews;
- iframes, HTML embeds, or live page embeds;
- automatically expanded cards.

This prohibition applies even when a connector can generate the preview. A failed preview is not a workflow gap and must not create a manual task.

## References and Recommended Reading

`References` contains only sources actually cited by numbered aliases in the publication body, and every numbered alias resolves to exactly one entry. A separate unnumbered `Recommended Reading` section may contain broader structural or pedagogical sources. Never label recommended reading as References, and never use a structural reading list in place of the sources supporting the published claims.

## Obsidian

Visible Obsidian notes normally link back to the relevant Notion chapter rather than duplicating the full bibliography. Internal lineage under `.gdkp/` preserves exact Notion and Zotero references. Add a direct source citation to a visible note only when it materially helps the learner and does not turn the note into a second textbook.

## Change Control

If a factual sentence changes meaning, re-run the Zotero claim audit before republishing. Pure formatting, link-label, or citation-number changes do not require user approval or a new source audit, but they require a fresh CitationProjection bound to the unchanged fact draft. Do not add a Notion or Obsidian read-back audit after the write.
