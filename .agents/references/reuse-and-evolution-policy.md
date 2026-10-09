# Knowledge Reuse and Evolution Policy

Reuse reads from an existing knowledge base for the current project. Evolution proposes writing current-project knowledge back into an existing knowledge base. They are separate optional decisions.

## Reuse Qualification

Inspect registry metadata first. A candidate is worth asking about only when it has meaningful goal coverage, usable source lineage, acceptable freshness, compatible scope, and a resolvable Notion and Zotero identity. A shared keyword or broad domain label is not enough.

Before Q3, present only a concise natural-language summary: knowledge-base name, origin project, relevant coverage, freshness, source basis, conflicts, limitations, and proposed mode. Do not show registry YAML.

Reuse modes:

- `reference`: consult the source knowledge base without copying it;
- `snapshot`: bind an immutable revision for reproducible use;
- `fork`: create new project-owned material with preserved lineage;
- `partial`: reuse only named topics;
- `none`: build independently.

Approved reuse creates internal ReuseLineage. It never authorizes changes to the source knowledge base.

## Evolution Eligibility

Propose evolution only when all of the following hold:

1. the new knowledge is supported by admitted evidence valid for the target knowledge base;
2. a concrete semantic relationship to an existing target node is explicit;
3. the addition improves the target knowledge base rather than merely resembling it;
4. Framework identifies the smallest suitable node or proposes a new concrete node;
5. Notion wording and likely Obsidian graph impact can be explained clearly;
6. the target project's managed scope is writable without touching user-authored content.

Keyword similarity, co-citation, shared hierarchy, or proximity is not sufficient.

## Q4 Presentation

In Codex, show:

- the existing topic that would change;
- the proposed addition in readable prose;
- why it belongs there and its source lineage;
- whether it adds or changes a graph relationship;
- the visible external marker and its effect;
- the option to decline without affecting the current project's result.

Do not show nested diffs, claim schemas, mutation envelopes, or cross-system receipts. Q4 approval binds the stated topic and change only.

## Placement and Marker

Insert an accepted external increment at the deepest suitable concrete Notion topic, not at a broad field or container merely because it is easy to find. Mark it with:

```text
※ External Increment
```

Machine behavior uses the internal origin status, not marker parsing. While status is `external_pending` or `external_accepted`, the increment remains excluded from the ordinary Obsidian graph. Do not remove the marker or promote the content automatically.

## Coordinated Update

After Q4 approval, Codex schedules the owning Skills in order:

1. Lifecycle validates the target project and managed scope.
2. Framework reserves the node and relation changes.
3. Zotero registers and audits evidence under the target policy.
4. Notion Author publishes the source-audited marked passage once and records the successful write result without a post-write content audit.
5. Obsidian refreshes the graph conservatively and honors exclusion rules.

Evolution skill plans and reconciles this work but does not write the three applications itself. Reversible in-scope writes proceed under Q4 authorization without separate technical previews. Any destructive, ambiguous, out-of-scope, or user-content-overwriting step requires a new direct decision.

## Refresh and Invalidation

Reassess reuse or evolution when source revisions, goal coverage, target structure, binding identity, or material conflicts change. A prior decline remains effective until the user reopens it or the material proposal changes.
