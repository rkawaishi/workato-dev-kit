---
name: learn-pattern
description: Record or update recipe construction patterns in `org/docs/patterns/recipe-patterns/`. Workato experts use this to accumulate know-how that helps others. Japanese prompts are also supported.
---

# /learn-pattern

A Workato expert records construction patterns into **`org/docs/patterns/recipe-patterns/`**.
The goal is to document know-how the expert already has. A reference recipe can be supplied as optional source material.

The write target is a single location in the org knowledge layer (the kit submodule's `docs/` is left alone). See `.cursor/rules/org-knowledge-overlay.mdc`.

## Usage

- `/learn-pattern` — start recording a pattern (interactive)
- `/learn-pattern "Pagination loop"` — specify the pattern name
- `/learn-pattern "Approval workflow" "additional caveats"` — append to an existing pattern
- `/learn-pattern <file-path>` — supply a recipe as reference material (the pattern itself is decided interactively)

## Procedure

### 1. Confirm the expert's intent

First survey existing patterns (read kit canonical and org sides; org wins on conflicts):
- `docs/patterns/recipe-patterns/_index.md` — kit canonical, generic patterns.
- `org/docs/patterns/recipe-patterns/_index.md` — org-recorded patterns (if present).
- `projects/docs/patterns/_index.md` — legacy org-domain patterns (if present; read-only for backwards compatibility).

Ask the user what they want to record:

```
What are we recording?

A. A new pattern (e.g. pagination loop, batch processing, etc.)
B. An addition to an existing pattern (caveats, variations, etc.)

Existing patterns:
- org/docs/patterns/recipe-patterns/: <list pattern names>
- (legacy) projects/docs/patterns/: <list pattern names if any>
```

Skip this question and proceed when the argument already makes the name / intent clear.

### 2. Interview the pattern

Ask the expert for the key points. You don't need to ask everything — build the structure from what they say:

- **When is it used** — what kind of requirement makes you reach for this composition?
- **Composition highlights** — which steps go where?
- **Why this composition** — why pick this over alternatives?
- **Gotchas** — pitfalls you only learn the hard way.

If a reference recipe is supplied, read the `.recipe.json` and summarize its structure for the expert. Use it to make the pattern concrete by cross-referencing the expert's description.

### 3. Write the pattern

Document the expert's know-how.

The write target is unified at **`org/docs/patterns/recipe-patterns/<pattern-name>.md`**.
Create the directory with `mkdir -p org/docs/patterns/recipe-patterns/` if it doesn't exist.

#### Template for a new pattern

```markdown
# <Pattern name> (<English Name>)

## Scope

- [ ] Generic — other organizations using Workato would reach the same composition
- [ ] Org-domain — tied to this organization's business or SaaS landscape

(Check whichever applies. Only "Generic" is a candidate for upstreaming to the kit.)

## When to use

| Condition | Applies |
|---|---|
| <condition 1> | Yes |
| <condition 2> | Optional |

## Recipe diagram

\```
[context]
    │
    ├── [Action/Loop/IF] <step description>
    └── ...
\```

## Step composition

| # | Provider | Action | Purpose |
|---|---|---|---|
| N | provider | action_name | description |

## Design decision points

| Decision | Recommended | Reason |
|---|---|---|

## Known gotchas

- <gotcha>

## References

- <related docs or patterns>
```

**Writing guidelines**:

- Write generic patterns in a form that **doesn't depend on any specific connector or organization**.
- Org-domain patterns can include concrete business processes and SaaS names.
- Abstract concrete recipe values (channel names, project names, etc.) when abstraction is possible.
- Put the "why this composition" reasons under design decision points.
- Capture the kind of implementation tips an expert would convey verbally under known gotchas.

#### Appending to an existing pattern

Before appending, grep for duplicates. Only add new insights:
- New design decision points.
- New gotchas.
- Variations of the composition.

### 4. Update the index

When you create a new pattern, add a row to the pattern list in `org/docs/patterns/recipe-patterns/_index.md`.
If the file doesn't exist, create it using the same format as `docs/patterns/recipe-patterns/_index.md` (kit canonical).

### 5. Confirm

Show the user the created / updated pattern file and confirm it is complete.
The most important thing is that the expert's know-how is captured accurately.

## Where things accumulate

The single write target is `org/docs/patterns/recipe-patterns/`. The generic / org-domain distinction is captured in the pattern's "Scope" section (not by path).

**Do not write to**:
- `docs/patterns/recipe-patterns/` (kit canonical, read-only).
- `projects/docs/patterns/` (legacy; existing files are read-only. New writes consolidate into the org side).

When valuable generic patterns accumulate for potential upstreaming, open a separate PR against the kit repository (out of scope here).

## Output

After completion, report:

- The created / updated pattern files with a content summary.
- If field-level knowledge also needs accumulating, point to `/learn-recipe`.

## Git management

The write target is in the workspace repository's `org/docs/patterns/recipe-patterns/` (outside the kit submodule):

```bash
cd <workspace-root>
git add org/docs/patterns/recipe-patterns/
git commit -m "docs(org): record pattern <pattern-name>"
```

**Do not commit to the kit submodule (`kit/`).**
