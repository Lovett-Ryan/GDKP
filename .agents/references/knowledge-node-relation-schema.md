# Knowledge Hierarchy and Relation Model

This model separates Notion's deep publication hierarchy from Obsidian's selective concept graph.

## Containers

A Container organizes publication scope: a discipline, domain, course, part, chapter group, product area, or other broad subject. It may have readable introductory content in Notion, but it is not automatically a graph node.

Containers may nest as deeply as the material requires. Hierarchy answers where a subject is taught; it does not by itself assert a semantic relationship.

## Knowledge Nodes

A KnowledgeNode is a concrete concept, method, mechanism, principle, event, argument, standard requirement, component, or reusable practice that can support a substantive explanation.

A good node:

- has a stable meaning in the project context;
- can be explained independently;
- matters to the goal or later reasoning;
- can carry evidence-backed content in Notion;
- may participate in explicit semantic relations, but may remain isolated when none is defensible.

Do not create nodes for empty headings, source titles, authors, tasks, validation states, metadata, or broad field names used only as organizational labels.

A KnowledgeNode is not a publication boundary. Do not infer that one node requires one chapter, heading, paragraph, or model call. A large-publication architect may group several related nodes into one teaching topic or expand one complex node across several topics and hidden DraftPackets while preserving every included content obligation.

## Hierarchy Versus Graph

Notion may contain every necessary chapter and subchapter. Obsidian should include only the subset of KnowledgeNodes whose presence improves understanding or recall. Therefore:

```text
Notion publication nodes >= Obsidian graph nodes
```

Membership in the same Container, page tree, source, or tag never creates an Obsidian edge.

## Relation Types

Use a small readable vocabulary and define the direction explicitly:

| Type | Meaning |
|---|---|
| `prerequisite_for` | Understanding or performing A is materially needed before B |
| `enables` | A makes B possible or practical |
| `causes` | A produces or materially contributes to B under stated conditions |
| `derives` | B follows from A by a stated derivation or transformation |
| `composes` | A is a functional part of B |
| `specializes` | B is a narrower form or case of A |
| `contrasts_with` | A and B differ along an important named dimension |
| `implements` | A realizes a rule, model, interface, or method B |
| `constrains` | A limits valid choices or behavior of B |
| `evaluates` | A measures or tests B |
| `applies_to` | A is usefully applied to B under stated conditions |

Add a domain-specific type only when none of these expresses the relation precisely. Record the natural-language explanation and evidence basis internally.

## Relation Quality

A relation is eligible when:

1. both endpoints are concrete nodes;
2. the direction and meaning can be stated in one or two clear sentences;
3. the relationship is important to the project goal;
4. its factual basis is supported by admitted evidence or source-audited published Notion content;
5. it is not a redundant transitive shortcut unless the direct link adds a distinct useful meaning.

Reject relations inferred only from proximity, shared keywords, shared citations, generic similarity, or model confidence.

## Relationship Content in Notion

When a relation is educationally important, Notion must contain a complete explanation in the most relevant chapter. It may appear as ordinary prose, a subsection, a comparison table, an example, or a toggle. The visible content never uses relation IDs or schema labels.

For a large publication, assign the relationship explanation to a teaching topic and bounded DraftPacket context without exposing those machine boundaries. A link, neighboring headings, or entries in RelationRegistry do not prove that the relation was explained in prose.

## Graph Selection

Obsidian chooses a cautious subset of nodes and relations. No center score or formal local-view center is required. Prefer important concepts with a small number of strong links; zero links is valid, and disconnected components are allowed. Never add a relation merely to make the graph connected. The internal GraphPlan records selection and exclusions so refreshes remain reproducible.

Importance tiers are presentation metadata, not semantic relations. They may control native graph color groups, while node size remains a consequence of actual link degree. The graph's actual edge set is the unique resolved Wikilink set in the managed notes and must equal the approved GraphPlan relation set.

## External Increments

Knowledge accepted from another project keeps an internal `origin_status` and a visible default marker `※ External Increment` in the target Notion passage. Insert it at the smallest suitable concrete node. While the status remains `external_pending` or `external_accepted`, omit that added passage and relations based solely on it from the ordinary Obsidian graph. Promotion is a separate future user decision; do not infer it from age or repeated use.
