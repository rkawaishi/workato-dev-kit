---
name: design
description: [Deprecated] Provides only legacy DESIGN.md view/update and `/design migrate` to convert into specs/. Use `/spec` for new projects. Japanese prompts are also supported.
---

# /design — Deprecated

> ⚠️ **This skill is deprecated.** Design for new projects has fully moved to the spec-driven workflow: `/spec` → `/clarify` → `/plan` → `/tasks` → `/analyze` → `/implement`.
>
> Only two responsibilities remain on `/design`:
> - **`/design migrate <project>`** — split an existing `DESIGN.md` into `specs/<NNN>-<slug>/{spec,plan,tasks}.md` (migration tool).
> - **`/design` / `/design update`** — backwards-compatible **read/update** for transitional projects still on DESIGN.md only (a deprecation warning fires every time).
>
> **`/design new` has been retired.** When invoked, refuse to run and point the user at `/spec`.

## Usage

- `/design <project-name>` — display the legacy DESIGN.md (with warning).
- `/design update` — update the legacy DESIGN.md to match the current implementation (with warning).
- `/design migrate <project-name>` — split the existing DESIGN.md into `specs/<NNN>-<slug>/{spec,plan,tasks}.md`.
- `/design new <project-name>` — **retired**. Refuse and point to `/spec`.

## Deprecation notice on entry

For any subcommand other than `/design migrate`, always display this warning before the main work:

```
⚠️ /design is deprecated (moved to the spec-driven workflow).
   New projects: /spec <project>
   Migrate existing DESIGN.md: /design migrate <project>

Continuing will only view/update the legacy DESIGN.md.
```

For `/design new`, do not proceed — return this message and exit:

```
❌ /design new has been retired.

Start design for new projects from /spec:
  /spec <project-name>          # create spec.md (requirements / WHAT・WHY)
  /clarify <project>/001-<slug> # resolve Open Questions
  /plan <project>/001-<slug>    # create plan.md (Workato configuration)
  /tasks <project>/001-<slug>   # break down into tasks.md
  /analyze <project>/001-<slug> # consistency check
  /implement <project>/001-<slug> # dispatch to the implementation skills

To move an existing project with DESIGN.md onto the spec-driven workflow:
  /design migrate <project-name>
```

The old hearing / design flow for `/design new` is fully removed from this skill. Do not accept it.

## Design-doc location (compatibility behaviour)

`projects/<project-name>/DESIGN.md`

`DESIGN.md` and `DESIGN.md.legacy.*` must be in the project's `.workatoignore` so they aren't wiped by `workato pull`. Both are part of the kit's base template (`templates/workatoignore.template`).

## Operations

### `/design` / `/design <project-name>` — view (with warning)

1. Display the deprecation warning above.
2. Read `projects/<project-name>/DESIGN.md`.
   - If missing: "No DESIGN.md found. Start the spec-driven workflow with `/spec <project-name>`." Exit.
3. Print the contents.
4. If there are unchecked items, suggest the next action — **and also recommend migrating to specs/ via `/design migrate <project-name>`**.

### `/design update` — update (with warning)

1. Display the deprecation warning above.
2. Read the current DESIGN.md.
   - If missing: "No DESIGN.md found. Start the spec-driven workflow with `/spec <project-name>`." Exit.
3. Inspect files in the project and identify implemented items:
   - `*.recipe.json` present → check recipe items.
   - `*.lcap_page.json` present → check page items.
   - `*.workato_db_table.json` present → check Data Table items.
   - `*.mcp_server.json` present → check MCP items.
   - `*.connection.json` present → check connection items.
4. Update the checklist.
5. Update `Status` and `Last updated`.
6. Append any new Decisions or Open Issues.
7. Display a summary of changes.
8. Finally recommend "Migrate to specs/ via `/design migrate <project-name>`".

### `/design migrate <project-name>` — DESIGN.md → specs/ migration

**Best-effort split** of an existing `DESIGN.md` into the spec-driven workflow artifacts (`spec.md` / `plan.md` / `tasks.md`). Because mapping cannot be fully mechanical, write ambiguous points into `Open Questions` / `Open Issues` so the user can continue with `/clarify`.

> Only this subcommand suppresses the deprecation warning (it is the very migration path we want to encourage).

#### Preconditions

1. Read `projects/<project-name>/DESIGN.md`. If missing, "No DESIGN.md found. Create one with `/spec <project-name>`." and abort.
2. If `projects/<project-name>/specs/` already exists and is non-empty, confirm:
   ```
   Artifacts already exist under specs/:
   - specs/001-foo/spec.md
   - specs/001-foo/plan.md
   
   What do you want to do?
   1. Abort (manual merge recommended)
   2. Generate in parallel as specs/002-migrated/
   3. Overwrite specs/001-foo/ (destructive, not recommended)
   ```

#### Determining the destination

- Feature slug: confirm with the user (defaults to `main` or derived from the project name).
- Sequence number: **follows the precondition outcome**:
  - `specs/` missing or empty → `001`.
  - Existing specs/ and **option 2 (generate in parallel)** chosen → max sequence under `specs/` + 1 (e.g. with `001-foo/` present, use `002`).
  - Existing specs/ and **option 3 (overwrite)** chosen → reuse the existing sequence number you target (e.g. choosing `specs/001-foo/` keeps `001`).
- Final path: `projects/<project-name>/specs/<NNN>-<slug>/{spec,plan,tasks}.md` (`<NNN>` is the sequence determined above).

#### Section mapping

Route each DESIGN.md section per:

| DESIGN.md section | Destination | Notes |
|---|---|---|
| `# <title>` | spec.md `# <title>` + plan.md `# <title> — Plan` + tasks.md `# <title> — Tasks` | Shared title |
| `## Status`, `Last updated` | `## Metadata` of each artifact | Propagate to spec/plan/tasks |
| Role-by-role steps under `## User Experience` | spec.md `## User Stories` | Copy nearly as-is |
| `## Architecture` `### Applied Patterns` | plan.md `## Applied Patterns` | Preserve pattern names and reference links |
| `## Architecture` `### Reused existing assets` | plan.md `## Reused Assets` | Asset names and uses |
| `## Architecture` `### New components` `- **Data Table**:` | plan.md `## New Components` `### Data Tables` | Includes field list |
| `## Architecture` `### New components` `- **Stages**:` | plan.md `## Stage Transitions` | Render as a transition diagram |
| `## Architecture` `### New components` `- **External integrations**:` | plan.md `## New Components` `### Connections` or spec.md `## External Touchpoints` | Provider-only goes to spec; technical detail to plan |
| `## Architecture` `### New components` `- **Recipe composition**:` | plan.md `## New Components` `### Recipes` | Split by main / Function / handler |
| `## Implementation Checklist` | tasks.md `## Tasks` | Infer and attach kind tags (see below) |
| `## Unlearned Actions` table | plan.md `## Unlearned Actions` table + `[learn]` tasks in tasks.md | Reflect in both |
| `## Decisions` | UX-flavoured → spec.md `## Decisions` / technical → plan.md `## Decisions` | Judge from text; when in doubt, send to spec |
| `## Open Issues` | plan.md `## Open Issues` | Post-deploy verification items go to plan |

#### Inferring kind tags for the Implementation Checklist

| Checklist phrasing | Inferred tag |
|---|---|
| "Data Table schema", "table" | `[data-table]` |
| "page", "form", "screen" | `[page]` |
| "recipe", "Recipe Function" | `[recipe]` / `[function]` |
| "connection", "auth" | `[connection]` |
| "MCP", "Genie", "skill recipe" | `[mcp]` |
| "pull", "learn-recipe" | `[pull]` / `[learn]` |
| "test", "verification", "E2E" | `[test]` |
| "custom connector", "connector.rb" | `[connector]` |
| None of the above | `[manual]` (also append to `Open Issues` for manual review) |

Dependencies are inferred best-effort (e.g. `[recipe]` after `[data-table]` and `[connection]`). For low-confidence cases, note `(depends: ?)` so `/analyze` can flag it.

#### Generating Open Questions / Open Issues

Write any items you cannot mechanically determine into one of:

- spec.md `## Open Questions`:
  - Unclear User Story roles.
  - Success Criteria not present in DESIGN.md (needs interview).
  - Out of Scope not made explicit (needs confirmation).
- plan.md `## Open Issues`:
  - Resources not fetched (should be fetched in Step 2).
  - Pattern-application items with low confidence.
  - Unclear stage transitions.
- tasks.md may always contain `[manual]` items that need manual review.

#### Post-migration processing

1. **Rename DESIGN.md to `DESIGN.md.legacy.<YYYY-MM-DD>`** (do not delete; keep for later reference).
2. Ensure `projects/<project-name>/.workatoignore` exists from the base template — copy `templates/workatoignore.template` if missing, otherwise append any missing entries (never remove lines):

   ```bash
   PROJ="projects/<project-name>"
   if [ ! -f "$PROJ/.workatoignore" ]; then
     cp templates/workatoignore.template "$PROJ/.workatoignore"
   else
     while IFS= read -r line; do
       case "$line" in ''|\#*) continue ;; esac
       grep -qxF "$line" "$PROJ/.workatoignore" || echo "$line" >> "$PROJ/.workatoignore"
     done < templates/workatoignore.template
   fi
   ```

   The template already covers `DESIGN.md`, `DESIGN.md.legacy.*` and `specs/`.

#### Result message

```
✓ Migrated: projects/<project-name>/

Generated files:
- specs/001-<slug>/spec.md         (<N> Open Questions)
- specs/001-<slug>/plan.md         (<M> Open Issues)
- specs/001-<slug>/tasks.md        (<T> tasks; <K> are [manual] and need review)

Renamed:
- DESIGN.md → DESIGN.md.legacy.<YYYY-MM-DD>

Next actions:
1. /clarify <project>/001-<slug>  — resolve Open Questions
2. /analyze <project>/001-<slug>  — verify consistency
3. /implement <project>/001-<slug> — continue implementation

Recommended review:
- Do the spec.md User Stories preserve the intent of DESIGN.md?
- Are the tasks.md kind tags reasonable? (If [manual] dominates, reclassify.)
```

#### Migration prohibitions

- **Do not delete DESIGN.md**: rename only. Never lose the source.
- **Do not overwrite specs/**: if specs/ already exists, take explicit user confirmation.
- **Do not carry unclear technical terms into spec.md**: if Workato terms (Recipe, datapill, Workflow App, etc.) leaked into User Experience in DESIGN.md, paraphrase them into business language for spec.md (when uncertain, file as Open Questions).

## Git management

Legacy DESIGN.md and `DESIGN.md.legacy.*` live under the workspace repository's `projects/`. After `/design update` or `/design migrate`, commit in the workspace repository:

```bash
git add projects/<project-name>/DESIGN.md* projects/<project-name>/.workatoignore projects/<project-name>/specs/
git commit -m "Migrate legacy design: <project-name>"
git push origin
```
