---
name: analyze
description: Verify spec.md / plan.md / tasks.md consistency. Run after /tasks and before /implement to catch drift between requirements and the implementation plan early.
---

# /analyze

Verify the **consistency** of `spec.md` ↔ `plan.md` ↔ `tasks.md`. Running this after `/tasks` and before `/implement` surfaces phase-to-phase drift early.

## Usage

- `/analyze <project>/<NNN>-<slug>` — verify a specific feature
- `/analyze <project>` — verify the latest feature in the project

## Workflow

```
/spec → /clarify → /plan → /tasks → /analyze → /implement
                                      ↑
                                   you are here
```

## Checks

### A. Completeness

- [ ] spec.md's `## Open Questions` has no unchecked items.
- [ ] plan.md exists.
- [ ] tasks.md exists.
- [ ] Each `Last updated` is not stale (spec newer than plan → plan may need regeneration).

### B. spec → plan trace

Verify that **every requirement in `spec.md` is addressed in plan**:

| spec element | Matches in plan | What to look for |
|---|---|---|
| User Stories roles | Pages/recipes operated by that role appear in `New Components` | Is there an action designed for each role? |
| External Touchpoints | Connections or Reused Assets in `New Components` | Does each mentioned service show up in Connections? |
| Success Criteria | Architecture Overview / Stage Transitions | Designed as observable state transitions? |
| Constraints | plan Decisions or Notes | Performance / security constraints reflected? |
| Out of Scope | plan stays out of those areas | Items the spec excluded are not built in plan |

**Mismatch examples**:
- spec says "notify the requester on rejection" but no recipe in plan covers it.
- spec's External Touchpoints lists "Confluence" but no Confluence connection in plan.
- spec's Out of Scope says "no delegated submissions" but plan has delegation logic.

### C. plan → tasks trace

Verify that **every New Component in plan is tasked**:

| plan element | Corresponding tag in tasks | What to look for |
|---|---|---|
| Data Tables | `[data-table]` | One task per table |
| Pages | `[page]` | One task per page |
| Recipes (main) | `[recipe]` | One task per main recipe |
| Recipe Functions | `[function]` | One task per function |
| Handlers | `[handler]` | One task per handler |
| Connections (new) | `[connection]` or `[manual]` | A task for each new connection |
| MCP / Genie | `[mcp]` | Has matching tasks |
| Unlearned Actions (rows) | `[learn]` | One `[learn]` task per unlearned row |

**Mismatch examples**:
- plan has 3 Data Tables but tasks has only 2 `[data-table]` tasks.
- plan's `Unlearned Actions` table has 2 rows but no `[learn]` tasks.
- tasks has a `[recipe]` that plan never describes (potential over-implementation).

### D. Deployment-guide compliance

Confirm `docs/patterns/deployment-guide.md`'s flow is embedded in tasks:

- [ ] `[validate]` precedes `[push]`.
- [ ] `[push]` exists.
- [ ] If there is a new connection, `[manual]` guides authentication.
- [ ] `[test]` exists.
- [ ] `[pull]` follows `[test]`.
- [ ] `[learn]` follows `[pull]` (when Unlearned Actions exist).

### E. Dependency sanity

- Is `[P]` honest?
  - Multiple recipes updating the same Data Table should not be `[P]`.
  - A recipe and a handler that references it should not be `[P]`.
- Do `(depends: N)` references point to tasks that exist?
- No circular dependencies?

## Procedure

### 1. Read the files

```
projects/<project>/specs/<NNN>-<slug>/
  ├── spec.md
  ├── plan.md
  └── tasks.md
```

If any of the three is missing, report what's missing and stop.

### 2. Run checks A–E

Go through each category in order and build an **issue list**.

Severity:
- **🔴 BLOCKER**: running `/implement` as-is will almost certainly break things (requirement uncovered, deployment guide violated).
- **🟡 WARNING**: needs attention but proceeding is defensible (over-implementation, possible drift).
- **🟢 INFO**: improvement suggestion (naming consistency, missing Decision entry).

### 3. Emit the report

Print to stdout in this format. **Do not write to a file** — the report is transient.

```
# /analyze report: <project>/<NNN>-<slug>

## Summary
- 🔴 BLOCKER: <N>
- 🟡 WARNING: <M>
- 🟢 INFO: <L>

## A. Completeness
✓ Open Questions: all resolved (<N>)
✓ plan.md / tasks.md: present
🟡 spec.md (2026-05-10) is newer than plan.md (2026-05-08); consider regenerating plan

## B. spec → plan trace
✓ User Stories (requester, approver, executor) → corresponding pages/recipes present
✓ External Touchpoints (Slack, Jira) → connections present
🔴 spec Success Criteria "notify requester on rejection" → no matching recipe in plan
🟢 spec Constraints says "response within 7 days"; plan has no mention (consider adding to Decisions)

## C. plan → tasks trace
✓ Data Tables (2) → 2 [data-table] tasks
🔴 plan.md Unlearned Actions has 2 rows but only 1 [learn] task
🟡 tasks has [recipe] approval_audit that plan never lists (possible over-implementation)

## D. Deployment-guide compliance
✓ [validate] → [push] → [manual] → [test] → [pull] → [learn] order OK

## E. Dependency sanity
✓ No circular dependencies
🟡 Task 5 [P] [page] and task 4 [page] may write to the same Data Table — reconsider parallelization

## Recommended actions
1. 🔴 Address spec's "rejection notification" in /plan (update plan.md, regenerate /tasks)
2. 🔴 Add a [learn] task for the second unlearned action (regenerate /tasks)
3. 🟡 Drop [P] from task 5 or make its order vs. task 4 explicit

Recommend not running /implement until BLOCKER count reaches 0.
```

### 4. Guidance

```
🔴 BLOCKER: <N>
  → Fix by re-running /plan or /tasks.

🟡 WARNINGS only:
  → Review, and proceed to /implement if you're satisfied.

🟢 INFO only:
  → Proceed to /implement.
```

## Rules to follow

- **Do not modify files**: `/analyze` is read-only. Fixing issues is `/plan` or `/tasks`'s job.
- **Leave the decision to the user**: don't mechanically block on WARNING — emit the report and defer.
- **Idempotent**: repeated runs produce the same report.

## Limitations

`/analyze` only checks **artifact-to-artifact consistency**. It does not verify correctness against Workato itself.
- Recipe JSON validity → `/validate-recipe`.
- Field schema correctness → re-run `/analyze` after `/learn-recipe`.

## Git management

`/analyze` writes no files, so no commit is needed.
