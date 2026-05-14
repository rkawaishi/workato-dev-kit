---
name: auto-learn
description: Drive the Workato UI through Claude in Chrome and autonomously collect every operation's field info for one connector, appending the results to `docs/connectors/<provider>.md`. Prefer autonomy over completeness — record uncertain cases and skip them rather than asking the user mid-run. Requires the Claude in Chrome extension and runs only in Claude Code. Japanese prompts are also supported.
---

# $auto-learn

Drive the Workato UI through Claude in Chrome and actively collect input / output fields for every operation (trigger / action) of the target connector, then append the results to `docs/connectors/<provider>.md`.

## Prerequisites

- **Editor**: Claude Code only (Cursor / Codex CLI / Gemini CLI cannot run this — they have no Chrome MCP).
- **Extension**: [Claude in Chrome](https://chrome.google.com/webstore) must be installed and connected. Without a connection, calls like `tabs_context_mcp` or `navigate` will fail (check connection state with `mcp__Claude_in_Chrome__list_connected_browsers`).
- **Workato login**: a tab signed in to the target workspace UI must exist (the skill does not log in for you).

## Design principles (important)

This skill is designed for **autonomy first, breadth second**. The goal is to **spread some level of field coverage across many connectors**, not to nail every type or nesting structure perfectly. Fine-grained corrections come later from manual recipes or `$learn-recipe`.

1. **No interaction**: a single invocation tries every op of the target connector. Do not ask the user mid-run. With no basis for a decision, **defaults → skip + log**.
2. **Fail-soft**: wrap each op in try / catch and keep going on failure. One op's failure does not abort the run.
3. **Record-driven**: append what you got, mark what you didn't as "learning failure / partial learning". Report at the end.
4. **UI only**: no new fetch / XHR against internal APIs (reverse engineering is strictly forbidden). Only **passive observation** of responses triggered by UI actions is allowed. See `docs/patterns/auto-learn-ui-operations.md`.

## Usage

```
$auto-learn <provider>
```

Options:
- `--recipe-id <id>` — recipe ID used for verification (default: inferred from the conventional recipe name or from the previous tab's URL).
- `--workspace-url <url>` — workspace base URL (default: previous tab).
- `--force` — relearn even if field details already exist in docs.
- `--triggers-only` / `--actions-only` — narrow the scope.
- `--sandbox <json>` — test data for dynamic schemas (see below).
- `--followups` — **no-UI mode**. Aggregate the `## Learning summary` sections of existing `docs/connectors/*.md` and print to stdout. A `<provider>` argument restricts to one connector; otherwise aggregates across all 7+ connectors. The execution flow (Phases 1–5) does not run. See "Followups mode" at the end of this file.

When prerequisites are missing (no conventional recipe, connection not authenticated, etc.), **exit with only a failure log — do not ask the user**.

## One-time setup (done by the user)

Set up the following in your verification workspace:

### 1. Conventional recipe (per connector, or one shared)

Recommended: project name `auto-learn-sandbox`, recipe name `<provider>` or shared `auto-learn-scratch`. **Fixed 4-step structure**:

| Step | Role | Default contents |
|---|---|---|
| 1 | **Trigger learning slot** | Anything (the skill overwrites it) |
| 2 | Bridging step | Any simple action (e.g. Google Sheets `Search rows` pointing at a low-column sandbox sheet). Anchors the predecessor step for the learning target and supplies output datapills |
| 3 | **Action learning slot** | Anything (the skill overwrites sequentially) |
| 4 | **Action output observation slot** | Any simple action (e.g. Workbot for Slack `Get user info`). A perch from which to peek at Step 3 output via Recipe data |

When `--recipe-id` is omitted, the skill:
- Uses the ID from the previous tab's URL if it matches `/recipes/<id>/edit`.
- Otherwise, **exits with only a failure log**.

### 2. Authenticated connection (target connector)

You can have several; the skill picks one per convention:

1. If `--connection <name>` is given, use it.
2. Otherwise pick "the **first active connection**" (DOM order of `w-connection-card`).
3. If neither exists, skip + log.

### 3. Sandbox data for dynamic schemas (only some connectors)

Required only when learning `extends_*_schema=true` style operations (Google Sheets `search_rows`, Salesforce variants, etc.).

- Pass via `--sandbox '{"spreadsheet":"auto-learn-sample","sheet":"Memo"}'`.
- Or read `scripts/sandbox-data/<provider>.json` (an optional repository convention).
- If neither exists, **silently skip** the dynamic probe and record only the static fields.

Keep the sandbox data **simple** (no duplicated headers, ~3 columns). Complex data triggers errors like `"duplicated headers"` and makes the dynamic input disappear.

## Execution flow

### Phase 1: Bootstrap

1. Read `docs/connectors/<provider>.md`.
2. Enumerate op name and kind from the Triggers / Actions tables.
3. Exclude: `__adhoc_http_action`, deprecated entries (rows annotated `[deprecated]` etc.).
4. Unless `--force` is set, skip ops that already have a section starting with `### <op>`. Match **by op name only** (the token right after `### ` at the start of the line); ignore parenthesised suffixes such as display titles. For example, both `### delete_message (Delete message)` and `### delete_message (Action)` count as the same op and are skipped.
5. Put the remaining ops into the processing queue.

### Phase 2: Tab preparation

1. Check existing tabs with `tabs_context_mcp`; create a new one if necessary.
2. Navigate to `/recipes/<id>/edit` from `--recipe-id` or the previous URL.
3. Confirm via DOM that the recipe has the 4-step structure (trigger + 3 actions). If not, log failure and exit.

### Phase 3: Run each op through `processOperation`

```
for op in queue:
    result = processOperation(op)        # wrapped in try/catch
    results.append(result)
    if result.errors:
        log warning, continue (do not stop)
```

Inside `processOperation`:

```
1. switchStepToOp(op)
   - kind=trigger → overwrite Step 1 (App tab → connector → Trigger picker → this op)
   - kind=action  → overwrite Step 3 (App tab → connector → Action picker → this op)
   - On failure (op invisible in the picker, auto-skip anomaly, etc.) → return result.status='failed_to_open' and **exit early** (skip steps 2–6 below)

2. waitForSetupTab()
   - Completion: button.tabs__label.tabs__label_active text === 'Setup'
   - Timeout 8 s. On timeout, **exit early** with result.status='failed_to_open'

3. result.input = captureInputFields()
   - If a "Show optional fields" button is present, open the modal and read {label, type, visibleByDefault} → Cancel
   - Enumerate top-level w-form-field in the form → {label, required, hint, controlComponent, hasToggleField}
   - Merge the two by label
   - If the button is absent, skip modal extraction (read only the form)

4. result.output = captureOutputFields(op.kind)
   - **Switch to the observation step before reading** (do not touch the target step):
     - kind=trigger:  open Step 2 → peek into the "Step 1 output" group of Recipe data
     - kind=action:   open Step 4 → peek into the "Step 3 output" group of Recipe data
   - If the data tree is minimised, expand it; click `.data-tree-group__header` of the target group
   - If the group never appears → record `null` ("no_output_schema" / fire-and-forget action)
   - If it appears → enumerate every `.data-tree-item` → {label, type}
   - ⚠ At the end you are still on the **observation step** (Step 2 / Step 4). Re-navigate before touching the target step again.

5. If result.input has dynamic picklist candidates (e.g. a select with w-toggle-field) and
   --sandbox is provided:
     // ⚠ Step 4 left you on the observation step — go back to the target step first
     // - kind=trigger: click the Step 1 (target) header to return to the Setup tab
     // - kind=action:  click the Step 3 (target) header to return to the Setup tab
     // Confirm the active tab is once again Setup via button.tabs__label_active before proceeding
     try {
       navigateBackToTargetStep(op.kind)         // re-open Step 1 / Step 3
       waitForSetupTab()                         // wait for the tab to return to Setup
       applySandboxValues()                      // fill the picklist on the target step
       const dynInput = captureInputFields()     // read the form on the target step
       const dynOutput = captureOutputFields(op.kind)  // internally switches to the observation step
       result.dynamic = { input: dynInput, output: dynOutput }
     } catch (e) {
       result.errors.push("dynamic_probe_failed: " + e.message)
     }

6. Finalise status:
   - If result.status is still unset (i.e. no early return in steps 1–2), set result.status = 'ok'
   - Errors[] presence does not affect status (partial learning is expressed as status='ok' + errors=[...])
   - ⚠ Cases that set 'failed_to_open' and early-returned in steps 1 / 2 never reach this point, so their status is not overwritten
```

### Phase 4: Append to docs

In `docs/connectors/<provider>.md`, append each op's result to the `## Action details` / `## Trigger details` sections:

```markdown
### <op_name> (<Display Title>)

Kind: Trigger | Action
Learned from: $auto-learn (UI observation) — <YYYY-MM-DD>[, output <YYYY-MM-DD>]

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| ... |

#### Output fields
| Field | Type | Description |
|---|---|---|
| ... |

#### Dynamic fields (if any)
- Decided by: <picklist name>
- Observed example: ... (avoid retaining PII)
```

Status is one of three values:

| status | Meaning | Set in |
|---|---|---|
| `ok` | processOperation completed end-to-end. Any individual issues in steps 3–5 (missing modal, missing output group, dynamic probe failure, etc.) are accumulated as strings in `errors[]`, but the status itself remains `ok` — treated as partial learning | step 6 |
| `failed_to_open` | Could not open the target op in step 1 / 2 and returned early | step 1 / 2 |
| `unexpected_error` | An unexpected exception escaped processOperation's internal try/catch and was caught at the outer loop | outer-loop catch |

⚠ Minor failures inside steps 3–5 use the **error-push approach instead of throwing** (treated as partial learning). Exceptions are only appropriate in steps 1 / 2 (the precondition to open the op broke) or for unexpected (bug) situations.

Append-routing rules (anything other than `'ok'` is treated as a learning-failure log):

- `status === 'ok'` & errors=[] → append the full section body.
- `status === 'ok'` & errors!=[] → add an annotation line (`> ⚠ Partial learning: <errors>`) and still append the section body.
- `status !== 'ok'` (=`failed_to_open` / `unexpected_error` / any future non-ok status) → do not create the section body; append one line to the `## Learning failures` section at the end of the file (`- <op>: status=<status>, reason=<reason> — <date>`).

### End of Phase 4: update the `## Learning summary` section (required)

After appending each op's result, add a `## Learning summary` section to the **end** of `docs/connectors/<provider>.md` (below the final `## ...` section). **Replace if it already exists** — this section holds only the latest run's snapshot, and historical runs are tracked via git history.

Format (assemble the fields from the run's results; lists separate op names with ` — `; if a set is empty, leave the line in place with `0`):

```markdown
## Learning summary

Last run: <YYYY-MM-DD> by $auto-learn
- Attempted: <N> op
- Fully learned: <M>
- Partially learned: <K>
- Failed: <L>
- Skipped:
  - Deprecated: <D> — `<op1>`, `<op2>`, ...
  - adhoc: <A> — `__adhoc_http_action`
  - Already learned: <S> — `<op1>`, `<op2>`, ...

### Needs follow-up

By category. Route entries using the prefix and reason in `errors[]`:

- **Dynamic schema (needs $learn-recipe)** — `dynamic schema unresolved`, `output_group_missing` (project not selected), etc.
  - `<op>` — <short note>
- **Fire-and-forget (UI spec — no further learning needed)** — `output_group_not_found`, `no_output_schema`
  - `<op>` — <short note>
- **Unknown internal key (needs $learn-recipe)** — internal key mapping unknown (e.g. `webhook_suffix`)
  - `<op>` — <short note>
- **Other** — partial-learning cases that fit none of the above
  - `<op>` — <reason>

Empty categories may be removed entirely (drop the heading too).

### Structural notes (for reference)

Copy each `> ⚠` inline note within an op section (other than `> ⚠ Partial learning:`) here, one per line:

- Duplicate label: `<label>` (op: `<op_name>`)
- Nesting hidden by paddingLeft=0: ...
- Dynamic input (depends on the input picklist): ...

Drop the heading entirely if there is nothing to record.
```

This section becomes **the single reference point for "give me follow-ups" requests**. `grep "^## Learning summary" docs/connectors/*.md -A 200` produces follow-ups for every connector.

`--followups` mode reads only this section to aggregate (does not run Phases 1–3). See "Followups mode" at the end of this file.

### Phase 5: Report

A short stdout report (must align with the `## Learning summary` written in Phase 4 — no drift allowed; copy-paste is fine):

```
$auto-learn <provider> complete
- Attempted: N op
- Fully learned: M op
- Partially learned: K op  (main theme: <theme>)
- Failed: L op  (reason: <reason>)
- Persisted: updated `## Learning summary` in docs/connectors/<provider>.md
- Items to feed back manually:
  - Duplicate labels: ...
  - Unresolved nesting depth: ...
  - Other observed irregularities: ...
```

End with the list of appended sections and a git-diff summary; let the user decide whether to commit (**do not auto-commit**).

When asked later to "produce follow-ups", you can answer just by reading the `## Learning summary` blocks in `docs/connectors/*.md`. The result is deterministically reproducible in a new session.

## Concrete rules for "don't stop"

| Situation | Response |
|---|---|
| No `Show optional fields` button | Skip modal extraction; read only the form |
| Trigger picker auto-skipped on single-trigger connector | Watch `tabs__label_active`. If you've jumped to Connection, skip the Trigger stage and use the default trigger |
| Step output group missing in Recipe data | Record `output: null` (fire-and-forget action) and continue |
| Picker title misprint (multiple ops with the same name) | Disambiguate by canvas step text or badge composition. Otherwise infer from DOM order + input contents on failure; last resort is skip + log |
| Dynamic picklist API error (duplicated headers etc.) | Retry once (with a different sandbox value if available). On second failure, give up and record only the static portion |
| Picker virtual scroll | When searching for an op, scroll → re-enumerate up to 3 times if not found |
| DOM stability wait | Prefer **mutation observation on specific selectors** (spinner disappear, tabs_label_active change, modal DOM appear/disappear) over `wait` |
| Click does nothing | Retry in order: parent-element click → `dispatchEvent(MouseEvent)` → physical coordinate click |
| Navigate blocked by `unsaved changes` | Just skip and continue with the recipe as-is (do not attempt reload) |
| Multiple connections | Argument → first in DOM → skip, in order. Do not attempt new auth dynamically |

## Completion selector catalogue

- Setup tab reached: `button.tabs__label.tabs__label_active` text === `Setup`
- Panel switch complete: `w-recipe-step-details w-panel-content` class becomes `recipe-step-config` or `recipe-step-details-adapter`
- Show optional fields modal open: `w-dialog label.multi-select-list__item` count ≥ 1
- Show optional fields modal closed: `w-dialog` removed from DOM
- Recipe data tree expanded: `w-datatree:not(.recipe-editor-datatree_minimize)`
- Step output group opened: `.data-tree-group_opened`

## Doc-update rules

- When a section already exists (relearning with `--force`):
  - Update the "Learned from" line to the latest date.
  - **Union-merge** the field table (replace same-name entries with the new info).
  - Leave a **trailing annotation** for duplicate labels (e.g. `> ⚠ The same label "User" appears twice. Internal path needs manual confirmation.`).
- New sections use the same format as [$learn-recipe](../learn-recipe/SKILL.md).

## Outstanding items (manual feedback required)

This skill targets "broad and shallow". The following cannot be captured by UI observation alone and are expected to be filled in manually:

- Duplicate labels (e.g. Slack `User`) — disambiguating internal paths for same-name fields.
- Data tree nesting depth (`paddingLeft: 0px` issue).
- Auto-exploration of chained dynamic picklists (spreadsheet → sheet → column).
- Mapping between internal `name` (JSON key) and display label (the UI shows only the label).
- Field-level `parse_output` / fine constraints (e.g. maximum character length).

When you notice any of these, either run `$learn-recipe` on a specific recipe or edit `docs/connectors/<provider>.md` directly.

## Error-handling design

All exceptions are **scoped to a single op's failure**:

```javascript
for (const op of queue) {
  try {
    const result = await processOperation(op);
    results.push(result);
  } catch (e) {
    // Even unexpected exceptions that pass through processOperation's try/catch advance to the next op
    // status='unexpected_error' is routed as a learning-failure log per the Phase 4 table
    results.push({ name: op.name, kind: op.kind, status: 'unexpected_error', errors: [e.message] });
    continue;
  }
}
```

Non-recoverable situations — tab died, network dropped, logged out, etc. — are the only cases that warrant early abort and an immediate report. Criterion: 3+ consecutive op failures → abort.

## Followups mode (`--followups`)

A **read-only aggregation mode** independent of the normal `$auto-learn` execution (no UI operations). It does not run Phases 1–5 at all — just reads the `## Learning summary` sections of `docs/connectors/*.md` and lists follow-ups.

### Invocation

```
$auto-learn --followups            # aggregate across all connectors
$auto-learn <provider> --followups # only the specified connector
```

### Behaviour

1. Targets:
   - With `<provider>` → `docs/connectors/<provider>.md` only.
   - Without → all of `docs/connectors/*.md` (exclude non-connector files like `_index.md` after content inspection).
2. Read each file and extract the `## Learning summary` section (up to the next `## ` or EOF).
3. Connectors without a section go into the `unknown` category as "uncollected" (left over from a past run).
4. Print a summary table and per-category follow-ups to stdout:

```
$auto-learn --followups (aggregated: 8 connectors / with learning summary: 7)

| Connector | Attempted | Full | Partial | Failed | Last run |
|---|---|---|---|---|---|
| gmail | 1 | 1 | 0 | 0 | 2026-04-27 |
| ...

Needs follow-up (per-category totals):
- Dynamic schema (needs $learn-recipe): 19
  - google_big_query: insert_row, search_rows_sync, ...
  - google_sheets: ...
- Fire-and-forget (UI spec — no further learning needed): 9
- Unknown internal key (needs $learn-recipe): 1

Uncollected (no `## Learning summary`; possibly a leftover from a past run):
- xxxx.md
```

### Design invariants

- This mode **does not touch the UI**. It does not invoke Chrome MCP. Only `Read` / `Grep` / `Bash` (grep) are used.
- `## Learning summary` is a **snapshot of the latest run**. Cumulative history is tracked via git (this mode does not).
- The `unknown` category surfaces "connectors with no section", encouraging a re-run.
- The mode produces no writes (**does not modify any doc files**).

### Judgement rule for existing sessions

When the user asks for "give me follow-ups" / "list the skipped ops" / "tell me what to feed back manually", Claude may either invoke `$auto-learn --followups` or implement the contents inline. What matters is using **`## Learning summary` as the sole reference point** (do not reconstruct from the table body or `> ⚠` inline notes — just read what was already aggregated).

## Git management

The write target is `docs/connectors/<provider>.md` inside the kit (submodule) only. The skill itself does not commit (the user decides at the end). Commit inside the kit and PR back to workato-dev-kit:

```bash
cd kit
git add docs/connectors/<provider>.md
git commit -m "auto-learn: <provider> N op (M ok / K failed)"
```

## Related skills / docs

- [$sync-connectors](../sync-connectors/SKILL.md) — collect Triggers/Actions lists (the upstream of this skill).
- [$learn-recipe](../learn-recipe/SKILL.md) — learn fields from an existing recipe (manual feedback path).
- [docs/patterns/auto-learn-ui-operations.md](../../../docs/patterns/auto-learn-ui-operations.md) — full DOM-selector reference for UI operations.
- [Issue #27](https://github.com/rkawaishi/workato-dev-kit/issues/27) — design motivation.
