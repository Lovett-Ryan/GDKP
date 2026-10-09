---
name: knowledge-framework
description: Design or revise an evidence-ready publication hierarchy, concrete KnowledgeNodes, ClaimIntents, semantic relations, and broad-domain coverage audit when required. Use before authoring when knowledge structure is needed; do not admit evidence, write publication prose, render the graph, or execute outcomes.
---

# Knowledge Framework

Design the internal knowledge model that lets Notion be complete and hierarchical while Obsidian remains selective and relational.

## Required References

Read [workflow-contracts.md](../../references/workflow-contracts.md) before handoff. Read [knowledge-node-relation-schema.md](../../references/knowledge-node-relation-schema.md) for hierarchy, node, and relation rules. Read [curriculum-coverage-policy.md](../../references/curriculum-coverage-policy.md) for a textbook, curriculum, comprehensive survey, field-level learning map, or other `coverage_first` project. Read [view-projection-policy.md](../../references/view-projection-policy.md) when identifying graph candidates. Read [claim-evidence-contract.md](../../references/claim-evidence-contract.md) before emitting ClaimIntents.

## Inputs

Require current ProjectContext, GoalContract, RequirementContract, SourcePolicy, and any approved ReuseLineage. Use admitted evidence when available, but allow an initial evidence-ready draft that exposes source gaps for focused work.

For `coverage_first` work, additionally require a current CoverageProfile, ScopeDecisionLedger, CoverageBaseline, and CoverageContract. Validate their project identity, revisions, checksums, and narrowing authority. A broad-domain framework without those inputs returns `needs_sources` or `needs_replan`; it must not silently fall back to model-memory coverage.

## Framework Design

1. Build a nested Container hierarchy appropriate to the subject and intended publication.
2. Define concrete KnowledgeNodes that can carry substantive explanations.
3. Treat KnowledgeNodes as coverage and evidence-planning units, not as mandatory chapters, headings, paragraphs, or authoring calls. Several related nodes may form one teaching topic, and one complex node may require several teaching topics.
4. Map requirements and learning or product outcomes to the smallest relevant nodes.
5. Create ClaimIntents for definitions, mechanisms, comparisons, formulas, constraints, examples, and other factual needs. For abstract theory, explicitly cover the modeled problem, variables, assumptions, inference target, objective, update or action, observable consequence, and validity boundary so the eventual application path is evidence-ready.
6. Define only explicit, useful semantic relations with readable reasons and evidence needs.
7. Identify important relationship or combination content that Notion must explain inside the relevant chapter.
8. Mark a cautious set of potential Obsidian graph nodes and defensible edges, allowing isolated candidates and disconnected components. Add a small editorial importance-tier candidate for presentation, but do not create a formal macro/local view pair, calculate a center score, or force connectivity.
9. Emit source gaps for unsupported ClaimIntents and revise after evidence admission when needed.

Framework structure is an AI-owned editorial and reasoning decision. Do not ask the user to approve IDs, hierarchy diagrams, relation registries, a ViewSpec, a center node, or a framework preview. Ask only through the orchestrator if a structural choice reveals a genuine goal ambiguity.

## Coverage-First Design

For a broad-domain framework, design against the CoverageBaseline rather than only the topics already named in the GoalContract.

1. Build the complete global field map before optimizing the teaching sequence.
2. Assign every baseline topic exactly one disposition: mastery, understanding, awareness, deferred, or excluded.
3. Keep major topics visible at awareness level when they are outside the learner's initial mastery set. Learner adaptation controls depth, not existence.
4. Map mastery, understanding, and awareness topics to concrete Containers or KnowledgeNodes. Record every deferred or excluded topic in an OmissionLedger with authority, learner impact, and a future route.
5. Check prerequisite closure for every mastery and understanding topic. Put supporting material in the main sequence, a just-in-time bridge, or a reference appendix; do not delete it.
6. Preserve disagreements among structural sources and record unresolved blind spots instead of manufacturing a single canonical taxonomy.
7. Generate source gaps both for planned ClaimIntents and for baseline topics that lack adequate structural or factual support.
8. Run [validate_coverage_audit.py](../../scripts/validate_coverage_audit.py) on the assembled CoverageProfile, ScopeDecisionLedger, CoverageBaseline, CoverageContract, TopicCoverageMatrix, and OmissionLedger.

Do not label the framework complete when only requirement mapping passed. Without a current passing coverage audit, return `needs_sources`, `needs_question`, or `needs_replan` as appropriate and keep the internal domain state `coverage_unverified`. A passing baseline whose status is `local_files_verified` yields `coverage_local_verified`; it can support framework review, but must retain the limitation that Zotero admission and factual-evidence use are still pending.

For a work too large to author in one pass, freeze the verified global hierarchy but do not project node boundaries directly into publication units or visible headings. Return the complete framework and traceable content obligations to the orchestrator so `large-publication-architect` can build the full-book chapter-to-knowledge map. Size changes scheduling and the number of bounded authoring calls, never silent topic removal or reduced local depth.

## Invariants

- Containers organize scope and do not automatically become graph nodes.
- A Notion child page may be useful even when it is absent from the Obsidian graph.
- Shared keywords, citations, tags, or page adjacency do not establish a semantic relation.
- Importance is presentation metadata and never establishes a semantic relation.
- Combination content must be complete in Notion; a link alone is insufficient.
- Stable IDs and machine types remain invisible in publication titles.
- KnowledgeNode count never determines visible heading count or DraftPacket count.
- External increments use the smallest suitable node and preserve their origin state.
- `Requirements covered` is not evidence that the domain is covered.
- A topic omitted from the framework cannot be represented as a source gap only after the fact; baseline reconciliation must make unknown omissions visible first.

## Outputs

Internally produce FrameworkSpec, ContainerRegistry, KnowledgeNodeRegistry, RelationRegistry, ClaimIntentBundle, SourceGapReport, and graph candidates. For `coverage_first` work, also produce TopicCoverageMatrix, OmissionLedger, and CoverageAuditReceipt. For `large_publication` work, expose the complete traceable framework input needed by `large-publication-architect` without deciding its teaching-topic, DraftPacket, paragraph, or visible-heading boundaries. Return `ready`, `needs_sources`, `needs_question`, or `needs_replan` to `knowledge-product-orchestrator`. `Ready` for broad-domain work requires a current passing coverage audit and must distinguish `coverage_verified` from `coverage_local_verified`. Zotero owns structural and factual source admission, the Architect owns the full-book chapter-to-knowledge map, Notion owns prose, and Obsidian owns final graph selection.
