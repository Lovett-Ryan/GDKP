# Notion Publication Model

This is an editorial model, not a rigid page schema. The Notion author chooses headings and block types that fit the subject, audience, and source material.

## Reader Experience

A knowledge project should read like a carefully edited textbook or monograph:

- natural chapter and section titles;
- a coherent explanation that can stand on its own;
- definitions introduced where the reader needs them;
- mechanisms, reasoning, formulas, examples, limitations, and applications integrated into the narrative;
- cross-topic combinations explained in the relevant chapter rather than delegated to an external link;
- citations at the claims they support;
- a clean References section.

Write for a capable reader. Be precise without rehearsing obvious meta-commentary, announcing every transition, praising the reader, or using a patronizing tutorial voice. Prefer connected explanatory prose over fragmentary cards and repetitive summary blocks.

For an unfamiliar or abstract theory, make its application path recoverable in the narrative: identify the problem, variables, assumptions, inference target, objective, update or action, practical consequence, and boundary. This is a reasoning spine, not a mandatory heading template. Use one running case only when it carries real explanatory work; otherwise use ordinary exposition and selective examples.

A product project may use Notion for a final manual, specification, decision document, or report only when that publication is part of the requested outcome. It must still read as a finished document, not as process telemetry.

## Adaptive Structures

Choose a structure by genre. Examples include:

### Concept or theory

Begin with the motivating problem, define the concept, explain how it works, develop consequences and limitations, and finish with connected ideas and references.

### Method, algorithm, or engineering technique

Explain the problem and assumptions, walk through the mechanism, include formulas or pseudocode when useful, discuss implementation choices and failure modes, then give an example and references.

### Historical, legal, social-science, or humanities topic

Establish context and terms, develop the argument or chronology, distinguish interpretations and evidence, discuss implications and limitations, then provide references.

### Product or standard

State the intended use and scope, explain behavior or requirements, provide procedures and examples, identify compatibility or risk boundaries, and provide references when external facts are used.

These are editorial prompts, not mandatory headings. Do not force every page into the same template.

## Nested Knowledge

Use Notion's nested pages when a large chapter contains coherent smaller subjects. The parent page should orient the reader and link naturally to its child pages. A child page remains a complete readable section, not an empty routing stub.

The internal Framework may distinguish Containers from KnowledgeNodes, but those machine types must not appear in visible titles or headings.

## Relationship and Combination Content

When two concepts interact, place a complete explanation inside the most relevant chapter or section. A toggle is often appropriate for optional depth. Include:

- why the relationship matters;
- the mechanism or constraint connecting the concepts;
- a concrete example, formula, comparison, or implication when useful;
- citations for factual claims.

A link to another page may support navigation, but it does not replace the explanation. Use a natural heading such as `Relationship to Layer Normalization`, not `Combination Block` or a machine identifier.

## Visible Content Rules

Do not show:

- stable IDs, revision numbers, checksums, evidence-unit IDs, audit states, or connector fields;
- headings such as `Base Capsule`, `Core Content`, `Verification`, or `Projection Package`;
- project questions, approvals, source-selection discussion, task state, or validation notes;
- system-generated exercises whose purpose is merely to verify the workflow.

Pedagogical questions or exercises are welcome only when they materially help the reader learn the subject.

Write inline mathematics as `$...$` and display mathematics as `$$...$$` in source drafts. Publish them as native Notion equation objects. Do not use Unicode approximations, mixed delimiters, fenced-code formulas, or raw delimiters as visible prose.

## References

Use numbered in-text citations such as `[1]` where appropriate. In the References section:

- format papers in IEEE style;
- use the page or site title for a webpage and include access context when useful;
- make the original URL directly clickable;
- never create a Source View image, screenshot, thumbnail, bookmark preview, iframe, or other embedded preview.

## Internal Authoring Cycle

The author first completes the substantive draft, then sends that complete draft through `notion-natural-prose-editor`. After the edited draft returns, the author resolves any substantive issues, extracts the final DraftClaimSet, requests an evidence audit, revises unsupported wording, publishes the audited revision, and verifies read-back. The prose editor does not own factual claims, citations, or publication. Those artifacts and iterations stay in Project Kernel state. Do not ask the user to approve a template profile, draft schema, block-by-block preview, or mutation receipt.

Read-back verification occurs after persistence and reload. Confirm the intended page hierarchy and section continuity, native equation objects with zero raw LaTeX delimiters, expected citations, clickable References, and preservation of user-authored blocks. A local or offline draft remains pending publication.

The actual published page is the review surface. If the user dislikes its wording, organization, depth, or style, revise the publication while preserving evidence integrity.
