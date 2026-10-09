# Architecture

[Documentation](README.md) | [Project README](../README.md)

GDKP separates orchestration, evidence, publication, learning views, and execution so each type of information has one clear home.

## Design Principles

- **Goal-driven:** work begins with an observable result and explicit acceptance conditions.
- **Coverage-aware:** broad knowledge maps are checked against approved structural sources instead of relying on model-memory enumeration.
- **Scale-isolated:** large publications grow by adding bounded `DraftPacket`s and checkpoints, not by compressing the depth of each knowledge point.
- **Evidence-gated:** Zotero registers and audits sources and matches evidence to exact publication claims before writing.
- **Audit-efficient:** successful Notion and Obsidian writes are not followed by routine content rereads or second-pass audits.
- **Reader-facing:** Notion contains finished publications rather than workflow operations.
- **Selective:** Obsidian contains useful concept notes and a sparse graph rather than a second copy of the publication.
- **Recoverable:** local revisions, hashes, handoffs, and checkpoints support reliable resume.
- **Outcome-oriented:** completion requires evidence of learning or a working deliverable.

## The Five Surfaces

| Surface | Responsibility | Must not become |
|---|---|---|
| **Codex** | Control plane, routing, user decisions, and completion reporting | Long-lived machine state or the canonical publication |
| **Zotero** | Source registry, structural coverage baseline, evidence admission, and claim audit | Draft prose or project task management |
| **Notion** | Canonical reader-facing textbook, monograph, report, or requested product document | Questions, task queues, audits, receipts, or workflow chatter |
| **Obsidian** | Selective study notes and a sparse semantic graph derived from source-audited publications | A mirror of the complete Notion hierarchy |
| **Local project** | Machine state, installed skills, executable work, outputs, and recovery data | Credential storage or unrelated user content |

The default Zotero structure is one root-level `GDKP-<Project Name>` collection with no automatic subcollections. Notion uses one natural publication root under a user-approved parent.

## End-to-End Flow

```mermaid
flowchart TD
    A[User goal] --> B[Workspace and capability check]
    B --> C[Compact outcome and source intake]
    C --> D{Coverage-first scope?}
    D -- Yes --> E[Structural coverage baseline]
    D -- No --> F[Requirements and work packages]
    E --> F
    F --> G[Evidence-ready knowledge framework]
    G --> P{Large publication?}
    P -- Yes --> Q[Full-book chapter-knowledge map and DraftPacket plan]
    P -- No --> H[Source admission]
    Q --> H
    H --> I[Complete substantive draft]
    I --> J{Explicit prose-polish request or feedback?}
    J -- Yes --> S[Bounded natural-prose refinement]
    J -- No --> R{Large publication?}
    S --> R
    R -- Yes --> T[One bounded pre-publication semantic review]
    T -- Findings --> U[One local repair; no re-review]
    T -- Pass --> K[Exact Zotero claim audit]
    U --> K
    R -- No --> K
    K -- Evidence gap --> H
    K -- Pass --> L[Publish once in Notion]
    L --> M[Write selective Obsidian notes and graph once]
    L --> N[Execute learning or product work]
    M --> O[Verified project outcome]
    N --> O
```

`knowledge-product-orchestrator` is the only control plane. Every other skill owns one bounded responsibility and returns a validated handoff instead of modifying another skill's artifacts.

## Coverage-First Workflows

Textbooks, curricula, comprehensive surveys, field-level maps, and similarly broad goals use an additional coverage-first branch:

1. Approved structural sources establish what belongs in the field boundary.
2. Coverage breadth and per-topic learning depth are recorded independently.
3. A `TopicCoverageMatrix` maps baseline topics to the planned framework.
4. Every narrowing, deferral, or exclusion is recorded in an `OmissionLedger` with accountable authority.
5. A deterministic coverage audit must pass before the framework is treated as complete.
6. The verified global framework is frozen before large-scale authoring begins.
7. Completion requires every included publication target to be assigned to a completed publication unit or explicitly reclassified through the governed omission process.

Structural sources establish the outline boundary. They do not automatically support the factual claims inside chapters; factual evidence still passes through source admission and exact claim audit.

## Large-Publication Workflows

Large-publication architecture is independent of coverage breadth. A broad field survey may need both the coverage-first branch and the large-publication branch; a narrowly scoped but deeply developed monograph may need only the latter.

Before prose begins, `large-publication-architect` produces one complete, human-readable `FullBookChapterKnowledgeMap`. It preserves every confirmed substantive knowledge obligation, groups related points into coherent teaching topics, and separates five granularities that must not be projected one-to-one: Framework nodes, teaching topics, hidden `DraftPacket`s, prose paragraphs, and visible headings.

The orchestrator then processes bounded packets automatically. Each packet receives its complete local knowledge obligations plus only the global context needed for continuity. Accepted drafts or stable page destinations, queue state, single-pass draft-review state, Zotero claim-audit state, publication-operation state, and next intent are persisted in external checkpoints. Runtime compaction may shorten the conversation, but it cannot advance completion state or replace those checkpoints.

The chapter-to-knowledge map and `PublicationCoverageIndex` assign every knowledge obligation to a bounded Packet and intended page before writing. Each coherent large-publication draft then receives one independent semantic review before claim extraction. It checks only whether assigned mechanisms, derivations, boundaries, applications, and relationships are actually explained; findings receive one local repair or a governed source/scope route, never a recursive re-review. Zotero then audits the final factual wording. Successful Notion and Obsidian writes end with their returned operation results. Later user feedback routes a targeted revision, and factual changes return to Zotero before republishing.

Scale therefore increases packet and model-call count rather than reducing local explanatory depth. A user-visible run completes the whole requested publication without stopping after chapter one or asking the reader to finish exercises. Exercises remain a separate, non-blocking learning branch unless the user explicitly requests an interactive chapter-unlock course.

## Project State and Outputs

| Path | Purpose | Version-control guidance |
|---|---|---|
| `.agents/` | Project-scoped GDKP skills and shared runtime resources | Version the approved core snapshot and reviewed project skills |
| `.knowledge-product/` | Bindings, checkpoints, hashes, receipts, and internal machine artifacts | Keep local by default; never publish credentials or machine-specific bindings |
| `Obsidian/` | Project-local Vault with selective concept notes and native graph settings | Decide per project and preserve user-authored notes |
| `outputs/` | Requested files, software, reports, exercises, or other deliverables | Decide per project and data-sensitivity policy |

Machine YAML, JSON, hashes, handoffs, and audit receipts stay out of routine user review. Users review the actual publication, knowledge view, product output, and verified acceptance result.
