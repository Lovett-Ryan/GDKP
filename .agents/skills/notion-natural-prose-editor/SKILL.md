---
name: notion-natural-prose-editor
description: Refine evidence-backed Notion textbook drafts into natural, technically dense prose with plain explanation by default, a running case when unfamiliar material needs one, and strict LaTeX, while preserving every factual claim, citation, definition, and limitation. Use after substantive drafting and before claim audit; do not create new evidence or publish pages.
---

# Notion Natural Prose Editor

Refine a complete textbook draft without changing its evidence-bearing substance. This Skill adapts the useful surface-editing discipline of an academic De-AI pass to reader-facing Notion chapters.

## Required Contract

Read [workflow-contracts.md](../../references/workflow-contracts.md) before handoff. For Chinese technical textbooks, also read [notion-prose-style.md](references/notion-prose-style.md).

## Inputs and Boundary

Require the complete draft, its intended audience, GoalContract, framework, current citations, and declared mathematical notation. Read the entire draft before editing.

Preserve claims, qualifications, numerical values, citations, variable meanings, definitions, assumptions, counterevidence, and section scope. Do not add factual claims or sources. If stronger application guidance would require a new claim, return a sourcing gap instead of inventing support.

This Skill edits local draft prose only. It does not own the Notion page, claim audit, source gate, or publication operation.

## Editorial Pass

1. Identify the dominant reading failure: unclear application path, thin explanation, repetitive rhythm, generic transitions, inflated tone, or patronizing metacommentary.
2. Choose the explanation mode. Default to clear ordinary exposition through definitions, mechanisms, derivations, and consequences. Do not force a case into familiar material that is already understandable on its own.
3. When the domain is unfamiliar, highly abstract, cross-layer, or counterintuitive, use one running case if it materially lowers the reader's reconstruction burden. Track the problem, model variables, assumptions, inference target, objective, update or action, observable consequence, and failure boundary; keep the mapping stable across sections and state where the analogy stops.
4. Deepen short sections by completing missing reasoning between definitions and consequences. Do not pad with summaries, slogans, or repeated paraphrase.
5. Remove generic AI phrasing, staged enthusiasm, rhetorical packaging, and repeated list templates. Vary paragraph and sentence length according to the argument.
6. Address a competent reader directly through precise exposition. Do not tell readers that a concept is easy, obvious, confusing, or all they need to know.
7. Audit every causal connective. Use derivational language only when the preceding equations or assumptions entail the conclusion.
8. Normalize every mathematical expression to the LaTeX contract below.
9. Read the revised draft continuously. In ordinary-explanation mode, confirm that each section remains self-sufficient; in case-assisted mode, confirm that the running case still clarifies rather than displaces the theoretical argument.

## LaTeX Contract

- Use `$...$` for inline mathematics and `$$...$$` for display mathematics in the Markdown draft.
- Never wrap mathematics in backticks and never use Unicode operators as substitutes inside formulas.
- Prefer `\mathbb{E}_{q}`, `D_{\mathrm{KL}}`, `\ln`, `\mid`, `\lVert`, and explicit subscripts and superscripts.
- Define symbols before first use and keep the same symbol for the same quantity throughout the publication.
- Put multi-step derivations in display blocks, one logical equality or implication per line, using `aligned` when useful.
- Keep prose punctuation outside inline delimiters unless it belongs to the mathematical expression.
- Before handoff, verify delimiter correctness and leave an explicit renderer check for `notion-node-author`; only that publication owner may claim that Notion produced native equation objects rather than literal dollar-delimited text.

## Output

Return the revised Markdown draft plus a private revision memo for Project Kernel. The visible draft contains no edit log, workflow commentary, quality score, or statement that it was De-AI processed.

Return to the orchestrator with `ready_for_claim_audit`, `needs_evidence`, or `needs_replan`.
