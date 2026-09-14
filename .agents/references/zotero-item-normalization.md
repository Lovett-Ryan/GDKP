# Zotero Project Collection and Item Normalization

Use this policy when registering, matching, normalizing, or auditing project sources.

## Project Collection

The default collection is:

```text
My Library
`-- GDKP-<Project Name>
```

Create it directly under the active library root. Do not create automatic subcollections by source type, chapter, status, or topic. Tags and internal project records carry those distinctions.

After creation, bind the project to the Zotero collection key. Reuse an existing collection only when the stored binding or an explicit user choice establishes identity. A title match by itself is ambiguous.

## Source Authorization

- Sources explicitly named by the user during the confirmed intake are pre-authorized for registration in the project collection.
- AI-suggested supplemental sources require one concise shortlist decision.
- Once a batch is authorized, routine create, import, collection-membership, metadata-normalization, deduplication, and verification operations within the project collection do not require item-by-item approval.
- Ask only for an ambiguous duplicate, a source outside policy, a paid or inaccessible source, destructive removal, overwrite of user-curated metadata, or another material risk.

## Canonical Source Types

Normalize papers, books, chapters, standards, laws, webpages, courses, videos, repositories, datasets, records, and private user material without forcing everything into an academic-paper schema. Preserve the original source type and the fields needed to identify its exact version.

## Identity and Deduplication

Prefer stable identifiers in this order when applicable:

1. DOI, ISBN, standard number, legal identifier, dataset DOI, repository commit, or other type-specific identifier;
2. canonical URL plus version or publication date;
3. normalized title, creator, publisher, and date;
4. content fingerprint for a user-provided local file.

Do not merge records based on title alone. Distinct editions, standards revisions, webpage versions, repository commits, jurisdictions, translations, and dataset releases remain distinct items. An ambiguous match is a user decision if merging would overwrite curated data; otherwise keep both and flag the ambiguity internally.

## Required Metadata

Capture as available and relevant:

- exact title and creator or responsible organization;
- source type, publisher or venue, date, edition, version, jurisdiction, and language;
- stable identifier and original URL;
- access date for volatile web sources;
- Zotero item key and project collection key;
- access limitations, license, retraction or supersession status, and known conflicts;
- user-primary or supplemental role;
- locator capability for claim-level evidence.

Never fabricate absent metadata. Preserve the original value when normalization is uncertain.

## Evidence Readiness

A Zotero record is registered but not admitted until the source content is available at the locator granularity needed by the intended claim and has passed relevance, authority, currency, version, jurisdiction, independence, and conflict checks. A bibliographic record or abstract alone supports only what it actually states.

Create locator-specific EvidenceUnits internally. Keep rejected, stale, inaccessible, duplicate, superseded, or contradictory material visible to the audit process without treating it as accepted support.

## Write and Verification

Use stable operation IDs, write only inside the bound project scope, re-read each created or updated record, and verify identity, metadata, and collection membership. Do not reorganize unrelated Zotero library content or delete an item merely because it is rejected for one project.
