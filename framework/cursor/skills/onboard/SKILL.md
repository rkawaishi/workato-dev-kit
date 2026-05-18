---
name: onboard
description: First-time onboarding for a workspace that already has Workato projects and custom connectors. Thin orchestrator that pulls every project and runs the existing learn / sync / catalog skills to bootstrap the org knowledge base. Japanese prompts are also supported.
disable-model-invocation: true
---

# /onboard

Bootstrap the organization knowledge base from **Workato assets that already exist** before the kit was adopted.

Most teams adopt this kit when their Workato workspace is already full of projects and custom connectors. `/onboard` pulls all of that down and runs the existing learn / sync / catalog skills over it, so `docs/` and `org/docs/` start out populated with the patterns, built-in actions, schemas and connector details this organization actually uses — making every later `/create-recipe` and `/plan` sharper.

This skill is a **thin orchestrator**. It does not pull, learn, sync or catalog anything itself — it sequences the existing skills and never reimplements their logic.

## Usage

- `/onboard` — onboard every remote project and connector
- `/onboard --projects "<a>","<b>"` — limit to specific projects
- `/onboard --resume` — continue an interrupted run from the progress report
- `/onboard --dry-run` — show the plan and scope, execute nothing

## Skills it orchestrates

| Step | Skill invoked | Writes to |
|---|---|---|
| Pull | `/pull-project --all` (or `--projects`) | `projects/` |
| Connectors | `/sync-connectors --all` | `docs/connectors/`, `connectors/docs/` |
| Learn recipes | `/learn-recipe <project>` (per project) | `org/docs/` |
| Patterns | `/learn-pattern` | `org/docs/patterns/recipe-patterns/` |
| Catalog | `/catalog scan` | `projects/CATALOG.md` |

`/onboard` only invokes these — see each skill for its own behaviour.

## Progress report

`/onboard` keeps a single artifact, **`org/onboarding-report.md`**, that doubles as the resume checkpoint and the final summary. It is a checklist of steps and per-project status. `--resume` reads it and skips everything already marked `[x]`; a fresh run creates it.

```markdown
# Onboarding report
Started: <YYYY-MM-DD HH:MM>   Last updated: <YYYY-MM-DD HH:MM>
Scope: all remote projects   (or: projects a, b, c)

## Steps
- [x] Pull projects        (12/12)
- [x] Sync connectors      (8 pre-built, 2 custom)
- [ ] Learn recipes        (7/12 projects)
- [ ] Learn patterns
- [ ] Catalog

## Per-project (learn-recipe)
- [x] Sales - Common
- [ ] [App] IT Onboarding   ← resume here
...
```

## Procedure

### 1. Preconditions

- Confirm the Workato CLI is authenticated: `workato projects list --source remote --output-mode json` succeeds. If not, tell the user to run `workato init` and stop.
- `--resume`: read `org/onboarding-report.md`. If it does not exist, say so and start a fresh run.

### 2. Plan and confirm scope

- List remote projects (`workato projects list --source remote --output-mode json`).
- Resolve the scope: all projects, or the `--projects` subset.
- Estimate size and **warn for large workspaces**: hundreds of projects/recipes mean a long run and many API calls. Recommend `--projects` for a first pass, and remind the user the run is resumable.

```
Onboarding plan:
  Projects to pull:   <N>
  Connectors:         /sync-connectors --all
  Then per project:   /learn-recipe → /learn-pattern → /catalog scan

This may take a while on a large workspace and is rate-limited by Workato.
The run is resumable with /onboard --resume. Proceed? (Y/N)
```

With `--dry-run`, stop here after printing the plan.

### 3. Create / update the progress report

Create `org/onboarding-report.md` (or load it for `--resume`). Mark steps `[ ]`.

### 4. Step — Pull projects

Invoke **`/pull-project --all`** (or `/pull-project --projects ...` for a subset). This also places each project's `.workatoignore` (see `/pull-project`). Update the report: `Pull projects (<done>/<total>)`.

### 5. Step — Sync connectors

Invoke **`/sync-connectors --all`** — pre-built connectors via API into `docs/connectors/`, custom connectors parsed from `connector.rb` into `connectors/docs/`. Mark the step done with counts.

### 6. Step — Learn recipes (per project)

For each in-scope project, invoke **`/learn-recipe <project-name>`**. `/learn-recipe` appends incrementally to `org/docs/` and is safe to re-run.

- On a large workspace, dispatch each project's `/learn-recipe` as a separate **`Agent`** call so one project's recipe volume does not exhaust context.
- After each project completes, check it off in the report's per-project list. This is the resume granularity — an interrupted run continues at the first unchecked project.

### 7. Step — Learn patterns

Across the pulled recipes, identify recurring constructions (pagination loops, approval flows, error handlers, …) and invoke **`/learn-pattern`** for each. Skip constructs already present in `docs/patterns/recipe-patterns/` or `org/docs/patterns/recipe-patterns/` — learn only the delta.

### 8. Step — Catalog

Invoke **`/catalog scan`** to inventory shared Recipe Functions and connections into `projects/CATALOG.md`.

### 9. Summary

Finalize `org/onboarding-report.md` and print the summary:

```
Onboarding complete.

Collected:
- Projects pulled:        <N>
- Connectors documented:  <P> pre-built, <C> custom
- Recipes learned:        <R> across <N> projects
- Patterns recorded:      <K>

Most-used built-in actions (top 10):
  <provider>/<action>   ×<count>
  ...

Needs follow-up:
- Unlearned actions:      <list from /learn-recipe "Unlearned Actions">
- Projects skipped / failed: <list>

Suggested next step:
- /auto-learn <connector>   to deep-dive a heavily-used connector via the UI
```

Compute "most-used built-in actions" by tallying `provider` / action keywords across the pulled `*.recipe.json` files (a read-only scan — no new knowledge logic).

## Scale and resume

- **Resumable**: every step and every project is checked off in `org/onboarding-report.md`. `/onboard --resume` re-reads it and continues at the first unchecked item. A run interrupted by a timeout, rate limit or context limit loses no completed work.
- **Idempotent**: re-running a completed step is safe — `/pull-project` respects `.workatoignore`, `/sync-connectors` and `/learn-recipe` append/update rather than duplicate, `/catalog scan` regenerates. Re-running `/onboard` without `--resume` re-verifies each step.
- **Rate limits**: `--all` issues many API calls. If the CLI starts failing, stop, let the user wait, and resume with `--resume`.
- **Context**: dispatch per-project `/learn-recipe` as `Agent` calls (Step 6) so a large project does not blow the orchestrator's context.

## Editor support

`/onboard` is **CLI / API only** — it does not require a browser, so it runs in every editor (Claude Code, Cursor, Codex CLI, Gemini CLI). Browser-based deep collection is intentionally out of scope; the summary suggests `/auto-learn` (Claude Code + Chrome extension) as an optional follow-up for heavily-used connectors.

## Rules to follow

- **Don't reimplement**: `/onboard` never pulls, learns, syncs or catalogs by itself — it only invokes the owning skills. The single piece of state it owns is `org/onboarding-report.md`.
- **Check off reliably**: mark a step / project `[x]` only after the invoked skill actually succeeds. On failure, record it under "Needs follow-up" and continue.
- **Confirm before a large run**: always show the plan and project count first; recommend `--projects` for a first pass.
- **Never touch the kit's `docs/` destructively**: learning writes go to `org/docs/` via `/learn-recipe` (see `.cursor/rules/org-knowledge-overlay.mdc`).

## Git management

Onboarding produces a lot of files (`projects/`, `org/docs/`, `docs/connectors/`, `CATALOG.md`). Commit in the workspace repository once the user has reviewed:

```bash
git add projects/ org/ docs/ connectors/ AGENTS.md
git commit -m "onboard: bootstrap knowledge base from existing Workato assets"
git push origin
```

Connector docs under the kit's `docs/connectors/` are commits into the kit submodule — PR them back to workato-dev-kit separately (see `/sync-connectors`).
