# Curriculum and Broad-Domain Coverage

Use this policy when a learning goal or publication is expected to represent a field rather than answer one focused question. It prevents learner adaptation, time pressure, or model recall limits from silently deleting parts of the subject.

## Coverage-First Trigger

Enter `coverage_first` mode when any of the following materially applies:

- the requested product is a textbook, monograph, handbook, curriculum, course, or comprehensive survey;
- the topic is field-level or has an unusually large and uncertain boundary;
- the user asks for comprehensive, systematic, complete, broad, end-to-end, or reference-style coverage;
- a learner is likely to treat the resulting outline as a map of what exists in the field.

A focused chapter, narrow question, local product, or explicitly bounded tutorial does not require this mode. When the trigger is ambiguous and the choice would materially change scope, ask one concise question.

## Separate Breadth From Depth

Record coverage breadth and learning depth as independent decisions.

Coverage breadth may be focused, canonical foundations, broad field map, or reference-comprehensive. Learning depth is assigned per topic as awareness, understanding, or mastery. A weak foundation may change order, scaffolding, notation load, examples, and initial depth; it must not silently reduce the visible breadth of the field.

The following implications are invalid unless the user explicitly confirms them:

- `not required for mastery` therefore `absent from the outline`;
- `selected foundational models` therefore `other major model families do not need to be named`;
- `beginner` therefore `only a minimal topic set`;
- `not exhaustive of every paper or implementation` therefore `major canonical branches may be omitted`.

## Scope Decision Provenance

`intent-source-analysis` owns a revisioned ScopeDecisionLedger. For every material normalization, it records:

- the raw user fragment and anchor;
- the normalized clause;
- whether the transformation preserves, expands, narrows, excludes, or infers scope;
- the authority: explicit user statement, governing policy, admitted structural evidence, or AI judgment;
- confidence, question state, and affected downstream artifacts.

A narrowing or exclusion requires explicit user authority or a named governing policy. AI judgment alone may propose a narrowing but may not confirm it. If the material choice is unresolved, return `needs_question`. Downstream Skills must reject a narrowing whose authority cannot be traced through the ledger.

## Structural Sources

Structural sources establish what topics and relationships a curriculum should consider. They are distinct from factual evidence used to support publication claims.

Suitable structural sources include authoritative textbook tables of contents, recognized course syllabi, standards or competency frameworks, and high-quality surveys or taxonomies. Prefer multiple independent sources when one source may reflect a narrow school, application, era, or author preference. A single user-selected source may be used as the instructional spine, but its known boundary must remain visible.

`zotero-source-gate` owns the CoverageBaseline. It records source role, identity, version or date, independence, authority, scope, extracted topics and aliases, topic prominence, dependencies, disagreements, and known blind spots. Structural metadata or a table of contents may guide framework coverage, but it is not evidence for the factual claims inside a chapter.

AI-suggested structural sources use the ordinary one-time supplemental shortlist decision. User-specified structural sources acknowledged during intake are pre-authorized. Inspection is not admission: unavailable or unapproved candidates may inform a shortlist but may not be represented as an admitted baseline.

When Zotero is temporarily unavailable, an exact user-specified or user-approved local document may produce a degraded but auditable CoverageBaseline with status `local_files_verified`. Record its resolved location, lowercase SHA-256 content digest, extraction method, read-back verification, and user-authorization anchor. A passing framework audit based on that baseline uses `coverage_local_verified`, not `coverage_verified`. It may support framework comparison and confirmation, but it does not admit the document as factual claim evidence or authorize publication citations. Proposed, inaccessible, unhashed, or model-recalled sources remain `coverage_unverified`.

## Coverage Contract

`requirement-reconstruction` owns the CoverageContract for a `coverage_first` project. It combines confirmed intent with the current CoverageBaseline and records:

- breadth profile and the meaning of completeness for this project;
- required topic classes and depth-allocation rules;
- audience and prerequisite policy;
- source and recency boundaries;
- allowed exclusions and their authority;
- coverage acceptance tests and invalidation conditions.

Requirement coverage and domain coverage are different states. `requirements_coverage_complete` means all confirmed requirements are mapped. It must never be reported as `domain_coverage_complete` or `coverage_verified` without a passing external coverage audit.

## Framework Coverage Artifacts

For `coverage_first` work, `knowledge-framework` additionally owns:

- TopicCoverageMatrix: maps every baseline topic to mastery, understanding, awareness, deferred, or excluded;
- OmissionLedger: explains every deferred or excluded topic, authority, learner impact, and future route;
- CoverageAuditReceipt: binds the CoverageContract, CoverageBaseline, framework revision, matrix, omissions, and deterministic validation result.

Every baseline topic must have exactly one disposition. Mastery, understanding, and awareness require a concrete framework target. Deferred and excluded topics require an OmissionLedger entry. A core topic may not be excluded solely to reduce length, simplify a beginner curriculum, or fit one model turn.

Run [validate_coverage_audit.py](../scripts/validate_coverage_audit.py) on the assembled coverage audit. Without a current CoverageBaseline and passing audit, the framework returns `needs_sources` or `coverage_unverified`; it does not claim completeness. A passing `local_files_verified` baseline permits `coverage_local_verified` only, with its Zotero and factual-evidence limitation kept visible.

## Dependency Closure

The framework must expose the prerequisites needed to understand every mastery or understanding topic. A prerequisite may be taught just in time or placed in a reference appendix, but it may not disappear. When a prerequisite is intentionally deferred, state the resulting limit on downstream understanding.

## Large-Publication Execution

Freeze and verify the global outline before substantial authoring, then write bounded publication units without changing the approved scope silently. Track every included framework target in a PublicationCoverageIndex as pending, drafted, audited, published, or blocked.

Large size changes scheduling, not coverage:

- keep the complete global map visible;
- author and audit coherent parts or chapters incrementally;
- serialize writes to the same external publication target;
- re-run the coverage audit after a material framework revision;
- declare the publication complete only when every included target is verified or explicitly reclassified through the governed omission process.

## Completion Standard

A curriculum or broad-domain framework is coverage-verified, or locally coverage-verified under the degraded rule above, only when:

1. the breadth and per-topic depth policy are confirmed;
2. the CoverageBaseline is current and source-bounded;
3. every baseline topic is represented or governed by an omission;
4. prerequisite closure is checked;
5. source disagreements and unresolved blind spots remain visible internally;
6. the deterministic coverage audit passes.

Coverage verification does not mean every possible paper, implementation, application, or historical detail is included. It means the chosen field boundary is externally grounded and no major topic inside that boundary disappeared without an accountable decision.
