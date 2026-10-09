# Human Decisions and Question Gates

This policy defines every situation in which GDKP may interrupt autonomous work for a user decision.

## Presentation Rules

- Ask only in the Codex interface.
- Use the host's structured Question mechanism when available; otherwise use a direct end-of-turn question.
- Use natural Markdown prose or a shallow list. Never show internal YAML, JSON, hashes, handoff envelopes, receipts, or schema tables as the question itself.
- Ask one to three short questions at a time and explain why the answer changes the result.
- Do not ask the user to approve artifacts that the AI can safely validate itself.
- Do not place questions, answers, decision logs, or status messages in Notion or Obsidian.
- Reuse a valid prior answer. Silence is never approval.

## Normal Intake

### Brief confirmation

`intent-source-analysis` owns the only required intake conversation. It combines the former intent and policy prompts into one compact exchange when possible. Confirm only missing or materially ambiguous information:

1. whether the current goal is learning, product delivery, or a mixture;
2. the observable result and acceptance condition;
3. the sources already chosen by the user;
4. whether Codex may find supplemental sources and any limits on language, date, version, region, jurisdiction, cost, access, or exclusions;
5. any decision or work the user explicitly wants to retain.

For a textbook, curriculum, comprehensive survey, field-level topic, or other broad-domain goal, also separate two facts that are often conflated:

- coverage breadth: focused, canonical foundations, broad field map, or reference-comprehensive;
- learning depth: which topics must be mastered, understood, or merely recognized.

If the user says they want comprehensive awareness but mastery of only selected topics, preserve both clauses. Do not translate selective mastery into a narrower outline. A learner's weak foundation changes sequencing and scaffolding, not the visible field boundary. Ask a concise clarification only when breadth remains materially ambiguous.

A user-specified source named during intake is pre-authorized for project registration. The answer internally produces an IntentContract and SourcePolicy; those files are not shown for approval.

When the user clearly requests a very large publication or reports that an existing long work is shallow or disconnected, record the large-publication signal without adding a separate routing question. Do not ask the user to approve DraftPackets, checkpoints, technical batches, or routine continuation after the first chapter. A complete full-book chapter-to-knowledge map is an additional decision point only when the user explicitly reserved its confirmation.

### Supplemental source shortlist

`zotero-source-gate` asks once only when Codex proposes additional concrete sources. Present a concise list containing the title, source type or publisher, why it is useful, and any material limitation. Ask whether to use all, a stated subset, or none.

For `coverage_first` work, this same decision may occur before framework design and may identify sources whose role is structural coverage, such as textbook tables of contents, recognized syllabi, or field taxonomies. State that structural sources help determine what belongs in the outline but do not by themselves support the factual claims inside chapters. Do not create a second shortlist question later unless the materially different factual-evidence candidates were not covered by the first decision.

Do not ask again for:

- unchanged candidates;
- user-specified sources already acknowledged at intake;
- deduplication, metadata normalization, collection membership, or other routine processing inside the approved Zotero scope.

A changed source, version, jurisdiction, cost, or material risk requires a new decision only for the changed portion.

## Conditional Gates

| Gate | Owner | Ask only when | If declined |
|---|---|---|---|
| Q3: reuse | `knowledge-base-reuse` | A qualified existing knowledge base could materially reduce work or improve continuity | Build independently |
| Q4: evolve | `knowledge-base-evolution` | Current-project knowledge has a supported semantic relationship to an existing knowledge base and an update is actually useful | Leave the existing knowledge base unchanged |
| Q5: acquire a GitHub Skill | `domain-skill-acquisition` | A verified capability gap affects an outcome and an eligible candidate exists | Use the safe generic fallback or report the unmet acceptance condition |

### Q3 presentation

Show the knowledge base's natural name, origin project, relevant coverage, freshness, source basis, limitations, and the proposed reuse mode. Offer reference, snapshot, fork, partial reuse, or no reuse. Do not expose registry records.

### Q4 presentation

Show which existing topic would change, a readable summary of the addition, why it belongs there, source lineage, graph impact, and whether it will carry the visible external-increment marker. Ask for update, staged marked update, or no update. Do not expose a machine diff.

### Q5 presentation

Show the capability gap, repository and path, immutable commit, license, purpose, meaningful risks, scripts or dependencies, requested permissions, project-scoped destination, proposed `[Project]-[Field]` display prefix, and generic fallback. Installation, update, replacement, removal, or promotion outside project scope each requires authorization for the exact change.

## Safety Decisions

Ask for a direct approval outside Q1-Q5 when an action would:

- delete or irreversibly alter data;
- overwrite user-authored content;
- write outside the approved project or external binding;
- create a material charge;
- use or expose a secret, credential, or sensitive dataset in a new way;
- choose between ambiguous external objects or conflicting identities;
- materially expand the goal, source boundary, audience, or risk.

Routine reversible writes inside a confirmed GDKP-managed scope do not require another approval.

## Internal Decision Record

Record the prompt, normalized answer, owner, affected revisions, and a deterministic fingerprint in machine state. Do not create a user-facing approval Markdown file. A decision remains reusable until its governing goal, source policy, candidate set, target, risk, or requested permissions materially change.
