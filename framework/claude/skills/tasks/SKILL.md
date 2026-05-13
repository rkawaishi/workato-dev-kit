---
description: Read plan.md and break it into executable tasks in tasks.md. Parallel markers [P] and kind tags ([recipe]/[page]/[learn]/etc.) let /implement dispatch the work. Japanese prompts are also supported.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# /tasks

Break `plan.md` into an **executable task list** and write `tasks.md`.

This sits after `/plan` in the spec-driven workflow. Explicit tags and dependencies are what let `/implement` later dispatch each task to the right skill.

## Usage

- `/tasks <project>/<NNN>-<slug>` — generate tasks.md for a specific feature
- `/tasks <project>` — auto-pick the latest feature that has plan.md but no tasks.md

## Workflow

```
/spec → /clarify → /plan → /tasks → /analyze → /implement
                            ↑
                         you are here
```

## Procedure

### 1. Read plan.md

- Read `projects/<project>/specs/<NNN>-<slug>/plan.md`.
- If `tasks.md` already exists, switch to **update mode** (preserve check states, only append new items).

### 2. Extract tasks and tag them

For each section of `plan.md`, cut tasks out and apply a **kind tag** and a **parallel marker**.

#### Kind tag (mandatory; exactly one)

| Tag | Owning skill | Example |
|---|---|---|
| `[connection]` | (manual or done inside `/create-recipe`) | Create a connection JSON |
| `[connector]` | `/create-connector` | Implement a custom connector |
| `[data-table]` | `/create-workflow-app` | Create a Data Table schema |
| `[page]` | `/create-workflow-app` | Create a Workflow App page |
| `[recipe]` | `/create-recipe` | Generate a recipe JSON |
| `[function]` | `/create-recipe` | Generate a Recipe Function |
| `[handler]` | `/create-recipe` | Handler recipe (Slack buttons, etc.) |
| `[mcp]` | `/create-genie` | MCP server / Genie / skill |
| `[validate]` | `/validate-recipe` | Validate JSON structure |
| `[push]` | `/push-project` | Deploy to Workato |
| `[pull]` | `/pull-project` | Pull post-UI changes |
| `[learn]` | `/learn-recipe` | Learn an Unlearned Action |
| `[learn-pattern]` | `/learn-pattern` | Add a construction pattern to the catalog |
| `[manual]` | (user) | UI work like connection auth, resource config |
| `[test]` | (user or `/implement`) | End-to-end test |

#### Parallel marker `[P]`

Tag tasks with `[P]` when they have no dependency on each other and **can run in parallel**. `/implement` uses this marker to decide whether to fan out.

Examples:
- `[P] [data-table] requests table` and `[P] [data-table] approvals table` are parallel-safe.
- `[recipe] approval_main` and `[handler] slack_approve_handler` are not parallel-safe (the handler references the `as` of the main recipe).

### 3. Express dependencies

When the parallel marker alone is not enough, capture the order in the **task numbering** and add `(depends: <task-id>)` notes as needed.

```
1. [data-table] Create the requests table
2. [data-table] Create the approvals table
3. [P] [page] Submission form page (depends: 1)
4. [P] [page] Approval page (depends: 1, 2)
5. [recipe] Generate approval_main (depends: 1, 2)
6. [handler] Generate slack_approve_handler (depends: 5)
7. [validate] Validate all recipes (depends: 5, 6)
8. [push] Deploy to Workato (depends: 7)
9. [manual] Authenticate Slack/Jira connections (depends: 8)
10. [test] E2E: request → approval → ticket creation (depends: 9)
11. [pull] Pull UI adjustments (depends: 10)
12. [learn] Learn jira/create_issue (depends: 11)
```

### 4. Auto-expand Unlearned Actions

If `plan.md`'s `## Unlearned Actions` table has rows, expand them into `[learn]` tasks:

```
| provider | action/trigger | notes |
|---|---|---|
| jira | create_issue | has custom fields |
| servicenow | create_record | input schema unknown |
```

↓

```
- [ ] [learn] Document jira/create_issue via /learn-recipe
- [ ] [learn] Document servicenow/create_record via /learn-recipe
```

**Important**: place `[learn]` tasks after `[push]` → `[pull]` (post-implementation learning cycle).

### 5. Incorporate the deployment guide

Follow `@docs/patterns/deployment-guide.md`'s "recipe deployment flow" and always include these tasks:

1. `[validate]` — pre-push validation
2. `[push]` — deploy to Workato
3. `[manual]` — guide the user through auth for any new connection
4. `[test]` — UI test run
5. `[pull]` — pull UI adjustments
6. `[learn]` — learn Unlearned Actions
7. `[learn-pattern]` — add any new construction pattern

### 6. Write tasks.md

Use the template below.

### 7. Next-step guidance

```
✓ Created tasks.md: projects/<project>/specs/<NNN>-<slug>/tasks.md

Total <N> tasks (parallel-safe: <M>, learning: <L>)

Next, run /analyze <project>/<NNN>-<slug> to verify spec ↔ plan ↔ tasks
consistency, then /implement <project>/<NNN>-<slug> to execute.
```

## tasks.md template

```markdown
# <Feature name> — Tasks

## Metadata
- Status: Draft
- Created: <YYYY-MM-DD>
- Last updated: <YYYY-MM-DD>
- Spec: ./spec.md
- Plan: ./plan.md

## Progress
- Total: <N>
- Completed: <0>
- In Progress: <0>
- Blocked: <0>

## Tag Legend
- `[P]` runnable in parallel
- Kind tags: `[recipe]`, `[function]`, `[handler]`, `[page]`, `[data-table]`, `[connection]`, `[connector]`, `[mcp]`, `[validate]`, `[push]`, `[pull]`, `[learn]`, `[learn-pattern]`, `[manual]`, `[test]`
- `(depends: N, M)` predecessor task IDs

## Tasks

### Phase 1: Foundation

- [ ] 1. [P] [data-table] Create `<table_name>` (fields: <list>)
- [ ] 2. [P] [data-table] Create `<table_name>`
- [ ] 3. [connection] Create `<connection_name>` (provider: <provider>, new/existing)

### Phase 2: Flow implementation

- [ ] 4. [page] Submission form page (depends: 1)
- [ ] 5. [P] [page] Approval page (depends: 1, 2)
- [ ] 6. [P] [page] Rejection notification page (depends: 1)
- [ ] 7. [function] Manager-lookup Function (depends: 3)
- [ ] 8. [recipe] `approval_main` recipe (depends: 1, 2, 7)
- [ ] 9. [handler] `slack_approve_handler` (depends: 8)
- [ ] 10. [mcp] MCP server / skill recipe (optional) (depends: 8)

### Phase 3: Validation and deploy

- [ ] 11. [validate] Validate every JSON with /validate-recipe (depends: 8, 9)
- [ ] 12. [push] Deploy with /push-project (depends: 11)
- [ ] 13. [manual] Authenticate the new connection in the UI (depends: 12)
- [ ] 14. [test] E2E: request → approval → ticket creation (depends: 13)

### Phase 4: Learn & feed back

- [ ] 15. [pull] /pull-project to pick up UI adjustments (depends: 14)
- [ ] 16. [learn] Learn `<provider>/<action>` via /learn-recipe (depends: 15)
- [ ] 17. [learn-pattern] Catalog new construction pattern via /learn-pattern (if any) (depends: 15)

## Notes
<!-- Things /implement should watch out for, rollback conditions, etc. -->
- <note>
```

## Rules to follow

- **Kind tags are mandatory**: untagged tasks cannot be dispatched by `/implement`.
- **Be honest with `[P]`**: don't tag something parallel-safe if running it in parallel would break (recipes often reference the predecessor's `as`).
- **Don't drop learning tasks**: leaving `Unlearned Actions` un-`[learn]`-ed lets knowledge gaps pile up.
- **Do not rewrite plan.md's body**: if you want to change the design while tasking, re-run `/plan`.

## Git management

```bash
git add projects/<project-name>/specs/<NNN>-<slug>/tasks.md
git commit -m "tasks(<project>/<slug>): initial breakdown"
git push origin
```
