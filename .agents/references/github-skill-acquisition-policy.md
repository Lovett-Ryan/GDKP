# GitHub Skill Acquisition Policy

This policy governs project-scoped Skills downloaded from GitHub after a verified DomainCapabilityGap.

## Scope and Ownership

`domain-skill-acquisition` exclusively owns discovery, Q5, staging, audit, adaptation, installation, update, disablement, and removal. Install under:

```text
<project-root>/.agents/skills/<canonical-name>/
```

Do not install an acquired Skill into user or system scope as part of a project request. Promotion is a separate explicitly authorized action.

## Candidate Eligibility

Resolve every repository reference to an immutable commit. Inspect only the relevant repository path. An eligible candidate must have:

- a clear purpose that addresses the verified gap;
- a readable license compatible with intended use;
- inspectable instructions and supporting files;
- declared dependencies, tools, network and filesystem behavior;
- no unresolved instruction conflict or credential-harvesting behavior;
- a practical validation method;
- a provenance trail that can be pinned.

Reject candidates that require hidden downloads, destructive installation, unverifiable binaries, excessive permissions, takeover of core workflow authority, or silent updates. Prefer a narrow, maintained, well-documented Skill over a broad agent bundle.

## Read-Only Discovery

Before Q5, remote work is inspection only. Do not place candidate files inside the project, run candidate scripts, install dependencies, or use credentials. Resolve the requested branch or tag to a commit and prepare no more than three qualified options.

## Q5

Present a short readable comparison in Codex. For the recommended candidate include:

- repository, path, immutable commit, and license;
- the gap it fills and expected output;
- meaningful limitations and maintenance signals;
- scripts, dependencies, network use, filesystem access, and other requested permissions;
- project-scoped destination and proposed visible name;
- the generic fallback.

Do not expose the full candidate manifest unless the user asks for an audit. Authorization is valid only for the exact repository path, commit, content hash, project, destination, and permission set. A material staging mismatch requires a new Q5.

## Naming

Keep the canonical directory and frontmatter name machine-safe:

```text
<project-slug>-<field-slug>-<upstream-skill-slug>
```

Change the Codex front-end display name to:

```text
[Project Name]-[Field] <Upstream Skill Name>
```

Use an English display alias when the upstream or project label cannot be represented safely. Record the original names separately. The short description should include immutable provenance in a compact form, for example:

```text
GitHub Skill: owner/repository@1a2b3c4d
```

Do not use the display prefix as a substitute for the provenance lock.

## Audit and Adaptation

After Q5:

1. stage only the approved path at the approved commit outside the active Skill directory;
2. inventory instructions, metadata, scripts, assets, dependencies, hooks, symlinks, and executable files;
3. check path safety, secrets behavior, network use, destructive commands, instruction conflicts, license duties, and undeclared dependencies;
4. preserve `allow_implicit_invocation: false` when present and do not broaden invocation policy;
5. adapt only approved UI naming or path references;
6. record the exact adaptation diff plus upstream and installed tree hashes;
7. run safe validation without production accounts, secrets, or destructive operations;
8. atomically install without overwriting an existing Skill directory;
9. verify host discovery before reporting the capability active.

If the host requires restart or cannot discover the Skill immediately, report `activation_pending` rather than active.

## Provenance Lock

The project lock records installation ID, capability ID, repository, path, requested ref, resolved commit, license, upstream name and hash, installed name and hash, display name, approved and enforced permissions, audit result, adaptation diff, install time, status, and invoking task lineage.

A lock is provenance and authorization evidence, not a sandbox. State plainly when the host cannot technically enforce an approved restriction.

## Lifecycle

- Never follow a moving branch or tag silently.
- Quarantine content or hash drift.
- Treat update, replacement, removal, and user-scope promotion as new authorized changes.
- Preserve a tombstone after removal.
- On every invocation, verify the lock and record the task, inputs, outputs, commit, and status.
- Return the result to the owning core Skill through Codex; the acquired Skill never controls downstream routing.
