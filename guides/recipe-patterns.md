# Recipe construction patterns guide

A mechanism that catalogs the construction know-how Workato experts have as "patterns" and references them automatically during Recipe generation.

## What is a pattern

A pattern is a recurring playbook used when building Recipes. It can apply to an entire Recipe or to a single piece of logic within one.

- **Entire Recipe**: approval workflow (request → approval → follow-up processing)
- **Part of a Recipe**: pagination loop (fetch all records from an API)

## Catalog structure

The write target is consolidated to `org/docs/patterns/recipe-patterns/`. When reading, the kit canonical and legacy paths are also consulted.

| Catalog | Location | Author | Content |
|---|---|---|---|
| kit canonical | `docs/patterns/recipe-patterns/` | kit maintainers | Patterns common across the Workato platform. Read-only (users do not edit) |
| Org side | `org/docs/patterns/recipe-patterns/` | `/learn-pattern` | Patterns recorded by the organization. Both general and org-domain patterns are consolidated here |
| Legacy | `projects/docs/patterns/` | (no new writes) | Patterns recorded in older versions. Read-only for backward compatibility |

The distinction between general and org-domain is expressed in the "Scope" section of each pattern's body, not by file path.

`/create-recipe` and `/plan` consult all three catalogs, and conflicts are resolved in favor of the org side (`org/docs/`) (see `@.claude/rules/org-knowledge-overlay.md`).

## Pattern flow

```
An expert has know-how
  → record the pattern interactively with /learn-pattern
  → accumulated in the catalog

Another developer creates a Recipe
  → /create-recipe automatically references the catalog
  → proposes step composition based on the pattern
  → /plan also proposes patterns when converting spec.md → plan.md
```

## How to use /learn-pattern

```bash
# Record a new pattern
/learn-pattern pagination-loop

# Add caveats to an existing pattern
/learn-pattern approval-workflow add-caveat

# Record a pattern while referring to a Recipe
/learn-pattern projects/[App] IT Onboarding/Recipes/main.recipe.json

# Start from a conversation
/learn-pattern
```

The skill asks about the following key points:

- **In what situation it is used** — for what kind of requirements this composition applies
- **Composition essentials** — which steps to combine and how
- **Why this composition** — why choose this composition over alternatives
- **Pitfalls** — gotchas you will hit if you do not know them

You do not need to cover everything; the skill documents the conversation along a template.

## Pattern file structure

Each pattern has the following sections:

| Section | Content |
|---|---|
| When to use | Table of application conditions |
| Recipe composition diagram | Overall view of the steps (ASCII diagram) |
| Step composition | Table of Provider / Action |
| Design decision points | Table of decisions, options, and decision criteria |
| Known caveats | Bullet list of pitfalls |
| References | Links to related documentation |

## When patterns are consulted

When `/create-recipe` generates a Recipe, after interview completion, the pattern catalog is consulted during step composition design (Step 6).

1. Break down the requirements (e.g. "fetch all records from API and reflect to DB")
2. Identify the patterns matching each part (e.g. pagination loop + data sync)
3. Incorporate the step composition, design decisions, and caveats from the patterns to assemble the JSON

Patterns function not as Recipe-wide templates but as **building blocks to be combined**.
