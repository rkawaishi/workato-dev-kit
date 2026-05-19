---
name: implement
description: Thin orchestrator that dispatches tasks.md's unfinished tasks to existing skills ($create-recipe, $create-workflow-app, etc.). Does not implement anything itself.
---

# $implement

A **thin orchestrator** that dispatches the unfinished tasks in `tasks.md` to existing skills.

This skill itself does not generate JSON or implement anything — it merely routes each task to the appropriate existing skill by its kind tag. The implementation responsibility stays with `$create-recipe`, `$create-workflow-app`, etc. (to avoid double-implementing).

## Usage

- `$implement <project>/<NNN>-<slug>` — run the feature's tasks in order
- `$implement <project>/<NNN>-<slug> --task <ID>` — run a single task
- `$implement <project>/<NNN>-<slug> --phase <N>` — run the tasks in Phase N
- `$implement <project>/<NNN>-<slug> --dry-run` — preview only, do not execute

## Workflow

```
$spec → $clarify → $plan → $tasks → $analyze → $implement
                                                  ↑
                                               you are here
```

Recommended (not required): `$analyze` reports 0 BLOCKERS before running `$implement`.

## Tag → skill mapping

| Tag | Skill / action it dispatches to |
|---|---|
| `[connection]` | Handled inside `$create-recipe` (standalone tasks: manual or template-generated) |
| `[connector]` | `$create-connector` |
| `[data-table]` | `$create-workflow-app` (Data Table task) |
| `[page]` | `$create-workflow-app` (Page task) |
| `[recipe]` | `workato-builder` subagent (fallback: `$create-recipe`) |
| `[function]` | `workato-builder` subagent — Recipe Function flag (fallback: `$create-recipe`) |
| `[handler]` | `workato-builder` subagent — handler recipe (fallback: `$create-recipe`) |
| `[mcp]` | `$create-genie` |
| `[validate]` | `$validate-recipe` |
| `[push]` | `$push-project` |
| `[pull]` | `$pull-project` |
| `[learn]` | `$learn-recipe` |
| `[learn-pattern]` | `$learn-pattern` |
| `[manual]` | Tell the user what to do, wait for their completion confirmation |
| `[test]` | Tell the user the test scenarios, wait for their result |

## Procedure

### 1. Preconditions

- Read `projects/<project>/specs/<NNN>-<slug>/tasks.md`.
- If it doesn't exist, say "Run $tasks first." and stop.
- Recommend running `$analyze` (warn if it has not been run yet).

### 2. Collect unfinished tasks

- Pick lines starting with `- [ ]`.
- Inspect dependencies (`depends: N, M`) — if any predecessor is still open, the task is a **skip candidate**.
- List the tasks that can actually run.

```
Runnable tasks: <K> / unfinished: <N>

Up next (dependencies satisfied):
  3. [connection] Create connection_name
  4. [P] [data-table] requests table
  5. [P] [data-table] approvals table
  7. [function] Manager-lookup Function

Waiting on dependencies:
  6. [page] Submission form page (depends: 4)
  ...
```

### 3. Pick an execution mode

Offer the user:

```
Choose how to run:
1. Sequential: confirm each task before running it
2. Phase: run all tasks in the same Phase together
3. Single: specify a task ID (`--task`)
4. Dry-run: only preview, don't dispatch
```

When running by Phase, offer to **fan out** the `[P]`-marked tasks in parallel.

### 4. Per-task execution

For each task:

#### 4a. Pre-brief

```
========================================
Task <ID>: <tag> <description>
Depends on: <depends>
Owner skill: <skill name>
========================================
```

#### 4b. Pass context

Extract whatever the owning skill needs from `spec.md` / `plan.md` / `tasks.md`.

For example, for `[recipe] approval_main`:
- The definition of that recipe from plan.md's Recipes section (trigger, flow, inputs/outputs).
- plan.md's Resource Inventory (resource selections).
- plan.md's Reused Assets (shared Functions to reference).

#### 4c. Invoke the skill

Dispatch the task to its owning skill. `$implement` itself never generates JSON.

- **`[recipe]` / `[function]` / `[handler]`** — dispatch directly to the **`workato-builder` subagent** (asset type `recipe`), invoked through your editor's subagent mechanism. `plan.md` already holds the finalized design, so no interview is needed: pass the recipe definition, Resource Inventory and Reused Assets from Step 4b plus the target file paths. The subagent keeps the ~1000-line JSON out of this orchestrator's context, returning a short summary. (This is the generation half of `$create-recipe` Steps 7–9.) Only if your editor has no subagent support, invoke `$create-recipe <project>/<NNN>-<slug>` instead.
- **Other tags** — invoke the owning skill from the tag → skill table. `$create-workflow-app`, `$create-genie` and `$create-connector` each dispatch their own generation step to `workato-builder` internally.

> **Important**: `$implement` must not generate JSON itself. The `workato-builder` subagent and the owning skills own all implementation.

#### 4d. Confirm and check off

After the skill completes, verify the output:
- The expected files exist at the expected paths.
- Run a quick validation if appropriate.

If everything looks good, change the task line to `- [x]` and update `Last updated`.
If it failed, rewrite the line as `- [ ] <description> ⚠️ FAILED: <reason>` and ask whether to continue or stop.

### 5. End of phase / end of run

When you finish a Phase:

```
✓ Phase <N> complete
Completed: <K> / Failed: <F> / Remaining: <R>

Proceed to the next Phase?
```

When every task is complete:

```
🎉 All tasks complete

Summary:
- Generated files: <list>
- Learned actions: <list>
- Patterns added: <count>

Next-step candidates:
- $catalog scan (to refresh the shared-asset catalog)
- $spec for the next feature
```

## Parallel execution (`[P]` tasks)

When running by Phase, consecutive `[P]` tasks can be fanned out in parallel.

```
Phase 2 has 3 [P] tasks:
  4. [P] [page] Submission form page
  5. [P] [page] Approval page
  6. [P] [page] Rejection notification page

Run them in parallel? (Y/N)
```

Parallel execution dispatches each task as an **independent Agent call**. You can re-run only the failed ones afterwards.

> **Caution**: parallel execution consumes a lot of context. For 3+ `[P]` tasks, sequential is usually safer.

## Handling `[manual]` / `[test]`

These are user actions:

```
Task 13 [manual]: authenticate the new connections (slack_bot, jira)

Open the UI at:
  https://<workato-region>/folders/<folder_id>

Tell me when you're done ("done" / "failed").
```

Wait for the user's confirmation before checking the task off.

## Rules to follow

- **Don't implement it yourself**: `$implement` is an orchestrator. Recipe JSON etc. belongs to the owning skill.
- **Check off reliably**: success → `[x]`, failure → `⚠️ FAILED`. Never advance with an ambiguous state.
- **Honor dependencies**: never fan out in parallel if `depends:` says otherwise.
- **Prefer dry-run first**: before running a large batch, use `--dry-run`.

## Error handling

- Skill invocation fails → report the situation to the user; ask whether to stop or skip.
- Some parallel tasks fail → check off the successes, mark failures `⚠️ FAILED`, let the user decide.
- The tasks.md completion state disagrees with reality → ask the user and amend tasks.md.

## Git management

Whether to commit per task or per phase is up to the user. Default: per phase.

```bash
git add projects/<project-name>/specs/<NNN>-<slug>/tasks.md projects/<project-name>/Recipes/ ...
git commit -m "implement(<project>/<slug>): phase <N> complete"
git push origin
```
