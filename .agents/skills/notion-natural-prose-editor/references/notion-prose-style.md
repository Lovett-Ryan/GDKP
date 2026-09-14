# Chinese Technical Textbook Style

Use this reference when editing Chinese Notion textbooks or monographs.

## Reader Contract

Assume the reader is intelligent and willing to follow a real argument. Supply prerequisites and intermediate reasoning because the theory requires them, not because the reader needs reassurance.

Remove patterns such as:

- announcing that a topic is easy, difficult, often misunderstood, or worth noting;
- telling the reader to remember, first separate, simply think of, or only grasp a slogan;
- repeated phrases equivalent to "in other words," "the key is," or "this means" when the equation already carries the point;
- symmetrical bullet lists that replace a continuous argument;
- closing paragraphs that merely restate the section.

Prefer declarative definitions, explicit assumptions, worked transitions, and concrete consequences.

## Explanation Mode

Use clear ordinary exposition by default. Define specialized terms when they first matter, show the mechanism or derivation, and connect it to a concrete consequence. Do not add a simplified story when the argument is already readable without one.

Use a running case selectively when the field is unfamiliar to the intended reader, the theory spans several abstract layers, the objective or mechanism is counterintuitive, or the reader would otherwise have to reconstruct how the formal pieces operate together. A useful case must preserve a stable mapping between the example and the theory, accumulate structure across sections, and identify where the analogy no longer supports inference.

A case is an explanatory scaffold. It must not replace definitions, equations, evidence, limitations, or the direct statement of the theory.

## Application Spine

A theory chapter should let the reader answer these questions without reconstructing the chapter alone:

1. What real inference or control problem is being modeled?
2. Which variables are hidden, observed, controllable, and preferred?
3. What joint probability model connects them?
4. Which posterior or policy quantity is intractable or unknown?
5. Which objective is optimized, and under which assumptions?
6. What does one update change in beliefs or actions?
7. What observable behavior or decision follows?
8. Which stronger interpretation is not justified?

When case-assisted explanation is warranted, use one running example across theoretical sections to clarify these questions. A short example should accumulate structure rather than restart from zero after each definition.

## Explanatory Depth

Do not enforce a fixed subsection template. A subsection is complete when the reader can follow the transition from premise to mechanism to consequence. Definitions without a worked consequence are too thin; examples without the governing equation are anecdotal; equations without symbol definitions or a decision role are decorative.

Use tables only for genuine comparisons. Use callouts sparingly for assumptions or boundaries that would otherwise be missed.

## Chinese Prose

- Prefer precise verbs and concrete subjects over abstract packaging nouns.
- Vary sentence length; use short sentences for conclusions and longer sentences for derivations or qualifications.
- Avoid translated English connective chains and repeated colon-led lists.
- Preserve technical terms in English at first occurrence when the English form helps disambiguation.
- Keep criticism proportional: state exactly which formulation, assumption, or inference is challenged.

