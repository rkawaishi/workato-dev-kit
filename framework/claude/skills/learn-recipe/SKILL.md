---
description: Analyze recipe JSON and accumulate field info / pattern findings into the organization knowledge layer (`org/docs/`). Learn from pulled recipes to grow the org knowledge base. Japanese prompts are also supported.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# /learn-recipe

Analyze recipe JSON and append every finding directly into the **organization knowledge layer `org/docs/`**.
We don't accumulate findings in an intermediate file — we grow each doc directly.

All writes target `org/docs/<relative-path>`; the kit's `docs/` is left alone. See `@.claude/rules/org-knowledge-overlay.md`.

## Usage

- `/learn-recipe <file-path>` — analyze a specific recipe
- `/learn-recipe <project-name>` — analyze every recipe in a project
- `/learn-recipe` — analyze every recipe across every project

## What we learn and where it goes

Every write target is `org/docs/<relative-path>`. Read the kit's `docs/<same-relative-path>` first and **skip** anything already documented there (only write differences, corrections, and org-specific additions).

### 1. Field info (most important)

Extract input/output field schemas from each step.

Sources:
- `extended_output_schema` — action / trigger output fields
- `extended_input_schema` — action / trigger input fields
- `input` — the actual input value (including datapill references)
- `parameters_schema_json` — Genie / Function parameters (JSON string)
- `result_schema_json` — Genie / Function result (JSON string)
- `input.input.schema` — Custom Action request schema
- `input.output` — Custom Action response schema

**Destination**: the matching action / trigger section of `org/docs/connectors/<provider>.md`.

Format:
```markdown
### <action_name>

#### Input fields
| Field | Type | Required | Description |
|---|---|---|---|
| field_name | type | Yes/- | label |

#### Output fields
| Field | Type | Description |
|---|---|---|
| field_name | type | label |
| parent.child | type | label (nested) |
```

### 2. New providers / actions

When you find an unknown `provider`/`name` combination in a recipe (i.e. an action that doesn't appear in the kit's `docs/connectors/<provider>.md`).

**Destination**:
- Pre-built connectors → the trigger / action list table in `org/docs/connectors/<provider>.md`.
- Workato-internal providers → `org/docs/platform/workflow-apps.md` or `org/docs/platform/agent-studio.md`.

### 3. JSON-structure findings

New discoveries about recipe JSON structure (new keywords, unknown fields, unusual constructs, etc.) — anything observed within the org's recipes. Accumulate them in `org/docs/`.

**Destination**:
- General recipe-structure findings → `org/docs/learned-patterns.md` (file general findings you'd like to upstream to the kit later here).
- Logic (if / loop / error) → the relevant file under `org/docs/logic/`.

### 4. Datapill patterns

New datapill notations or reference patterns.

**Destination**: `org/docs/logic/data-pills.md`.

### 5. Deploy-related findings

New behavior observed on push/pull (field reset, schema expansion, version change, etc.).

**Destination**: `org/docs/patterns/deployment-guide.md`.

### 6. Findings that don't fit elsewhere

Anything that doesn't match the categories above.

**Destination**: `org/docs/learned-patterns.md` (temporary holding; move to the right file later).

## Analysis procedure

1. Read the target `.recipe.json`.
2. Walk every step recursively.
3. For each step:
   a. Check whether `provider` and `name` are known (consult both `docs/connectors/<provider>.md` and `org/docs/connectors/<provider>.md`).
   b. If `extended_output_schema` / `extended_input_schema` is present, extract the field info.
   c. Record any new structural patterns.
4. If the destination directory under `org/docs/<...>` doesn't exist, create it with `mkdir -p`.
5. Read the destination file and check for duplicates.
6. Read the kit-side `docs/<same-relative-path>` too; if the info is already there, **do not write it**.
7. Append only the new findings.

## Duplicate check

Before writing, grep both files for the same content:
- The destination `org/docs/<path>.md`
- The corresponding kit-side `docs/<same-path>.md`

- The kit already has field info for the same action → add only the diff (org-specific fields or corrections).
- The same rule already exists → skip.

## Output

After analysis, report:
- The number of files analyzed.
- The list of updated docs (all under `org/docs/`) with a summary of what was appended.
- Any newly discovered patterns.

## Reconciling Unlearned Actions

When run against a project, scan every feature's `plan.md` and `tasks.md` under `projects/<project-name>/specs/` and reconcile entries that correspond to the `provider` / `action` you just learned (see "Recipe implementation lifecycle" in `@.claude/CLAUDE.md`).

### `## Unlearned Actions` table in plan.md

For each `projects/<project-name>/specs/<NNN>-<slug>/plan.md`:

1. Check for a `## Unlearned Actions` table.
2. If a row matches the just-learned `provider` / `action`, **delete the row**.
3. When every row is deleted, leave the table in place with a note "(learned)" — keep it as a history record.

### `[learn]` tasks in tasks.md

For each `projects/<project-name>/specs/<NNN>-<slug>/tasks.md`:

1. Find unfinished tasks (`- [ ]`) tagged `[learn]` that mention `provider/action`.
2. Check them off as `- [x]`.
3. Update `Last updated`.

### Reporting

```
Unlearned Actions reconciliation:
- Rows removed from plan.md: <N> (in <feature> etc.)
- Tasks checked off in tasks.md: <M> (in <feature> etc.)

Features still carrying unfinished Unlearned Actions:
- <project>/specs/<NNN>-<slug>: <remaining count>
```

> **Backwards compatibility**: the legacy `## Unlearned Actions` in `projects/<project-name>/DESIGN.md` is **not read** (hard-cutover in Phase B). If a project still only has DESIGN.md, run `/design migrate` first to convert into `specs/`.

## Git management

Writes happen in the workspace repository, under `org/docs/` and `projects/<name>/specs/`:

```bash
cd <workspace-root>
git add org/docs/ projects/<name>/specs/
git commit -m "docs(org): learn from <project-name> recipes"
```

**Do not commit to the kit submodule (`kit/`).** When you accumulate general findings worth upstreaming, open a separate PR against the kit repository.
