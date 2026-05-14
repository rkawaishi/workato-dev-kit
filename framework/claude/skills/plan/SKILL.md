---
description: Read spec.md and write the Workato configuration (HOW) to plan.md. Consults the pattern catalog, CATALOG.md, and .resource-providers.yml to lock in technical choices. Japanese prompts are also supported.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# /plan

Map the requirements in `spec.md` into **Workato configuration** and generate `plan.md`.

In the spec-driven workflow this runs after `/spec` → `/clarify`. It only decides "how to build this in Workato". Splitting the work into executable tasks is `/tasks`'s responsibility.

## Usage

- `/plan <project>/<NNN>-<slug>` — generate plan.md for a specific feature
- `/plan <project>` — auto-pick the latest spec in the project that has no plan.md yet
- `/plan` — infer from the current session context

## Workflow

```
/spec → /clarify → /plan → /tasks → /analyze → /implement
                    ↑
                 you are here
```

Assumes `/clarify` has cleared every Open Question. If any remain unresolved, abort and ask the user to run `/clarify` first.

## Procedure

### 1. Preconditions

- Read `projects/<project>/specs/<NNN>-<slug>/spec.md`.
- If `## Open Questions` still has unchecked items, abort:
  ```
  <N> Open Questions are unresolved. Run /clarify <project>/<NNN>-<slug> first.
  ```
- If `plan.md` already exists, switch to **update mode** (respect existing content; only append diffs).

### 2. Auto-collect resource info

Read `.resource-providers.yml` and, for the external services mentioned in the spec's `External Touchpoints`, pre-fetch their resource info.

1. Skip if `.resource-providers.yml` doesn't exist (record "verify after deploy" in plan.md's `Open Issues`).
2. For each defined provider, follow `@docs/platform/resource-providers.md` to detect and run the relevant tool.
3. Examples of what to capture:
   - Jira project issue types and custom fields → reflect in Data Table field design.
   - Slack channel list → concretize the notification destination.
   - Google Sheets header row → field mapping design.

> **Important**: silently skip on fetch failure. Do not abort.

### 3. Check the shared asset catalog

Read `projects/CATALOG.md` and identify parts of the spec that **existing shared assets** can cover:

- Can a shared Recipe Function (manager lookup, notification sender, etc.) be used?
- Can a shared connection (Slack, Jira, etc.) be reused?
- Is there an existing Workflow App or pattern worth referencing?

If the catalog is missing, note "Can be generated with `/catalog scan`" in plan.md's `Notes`.

### 4. Check the pattern catalog

Identify **construction patterns** that match the user experience:

- `@docs/patterns/recipe-patterns/_index.md` (kit canonical)
- `@org/docs/patterns/recipe-patterns/_index.md` (org-side, if present)
- `@projects/docs/patterns/` (legacy, read-only for backwards compatibility)

The org version wins on conflicts. Bring the matching pattern's diagram, step composition, and known caveats into the plan.

### 5. Map to Workato configuration

Map each User Story in `spec.md` into Workato building blocks.

**Decision points:**

| User experience | Workato building blocks |
|---|---|
| Submit a form | Workflow App + Data Table + submission page |
| Approval flow | `human_review_on_existing_record` + stages |
| Slack notification with buttons | `slack_bot/post_bot_message` + `attachment_buttons` + `bot_command_v2` handler |
| Slack notification (informational only) | `slack_bot/post_bot_message` |
| Email notification | `gmail/send_email` or `human_review` email notification |
| Create an external ticket | `jira/create_issue`, ServiceNow, etc. |
| Look up data (e.g. manager) | Recipe Function (Google Sheets, HRMS, etc.) |
| API-driven submission | MCP server + skill recipe |
| Multi-stage approval | Multiple `human_review` + stages |
| Conditional branching | if/elsif/else |
| Update data | `update_request` / `workato_db_table` |

**How to split recipes:**

- Independently reusable logic → extract into a Recipe Function.
- Blocking actions (`human_review`) → keep in the calling recipe (do not put inside a Recipe Function).
- External triggers (Slack buttons, etc.) → separate recipe (link via `complete_task`).
- MCP-facing → skill recipe (`add_record` + workflow start).

### 6. Design decisions for the Workato API

If the design includes anything that talks to the Workato API (CLI/MCP, API Platform, OEM integration, etc.), always read the comparison table and decision flow in `@docs/platform/workato-api-systems.md` (to avoid confusing the four "API Client" systems and having to redesign).

### 7. Write plan.md

Use the template below.

### 8. Extract Unlearned Actions

Whenever you use a trigger or action that **lacks documentation** in Workato official docs or in `docs/connectors/` / `connectors/docs/`, populate `Unlearned Actions`. These get expanded into `[learn]`-tagged tasks by `/tasks`.

### 9. Next-step guidance

```
✓ Created plan.md: projects/<project>/specs/<NNN>-<slug>/plan.md

Architecture highlights:
- <3–5 entries summarizing the architecture>

Unlearned actions: <N> (need /learn-recipe after implementation)

Next, run /tasks <project>/<NNN>-<slug> to break this down into executable tasks.
```

## plan.md template

```markdown
# <Feature name> — Plan

## Metadata
- Status: Draft
- Created: <YYYY-MM-DD>
- Last updated: <YYYY-MM-DD>
- Spec: ./spec.md
- Project: <project-name>

## Architecture Overview
<!-- One-paragraph summary of the overall design + optional ASCII diagram. -->
<diagram or bullets describing the big picture>

## Applied Patterns
<!-- Patterns from the catalog that apply here. -->
- **<pattern>** (`docs/patterns/recipe-patterns/<file>.md`): <where it applies and why>
- **<pattern>** (`org/docs/patterns/recipe-patterns/<file>.md`): <where it applies and why>

## Reused Assets
<!-- Shared assets from CATALOG.md that we can reuse. "None" if there are none. -->
- **<shared function>** (`projects/<path>`): <purpose>
- **<shared connection>**: <purpose>

## New Components

### Data Tables
- **<table>** (`<project>/Data Tables/<file>.data_table.json`):
  - Fields: `<field1>` (string), `<field2>` (datetime), ...
  - Primary key / indexes: <definition>

### Pages
- **<page>** (`<project>/Pages/<file>.lcap_page.json`):
  - Role: <submission / review / approval / rejection>
  - Main components: <forms, tables, buttons>

### Recipes
- **<main recipe>** (`<project>/Recipes/<file>.recipe.json`):
  - Trigger: <provider/event>
  - Flow: <step summary>
- **<Recipe Function>**:
  - Purpose: <reusable logic>
  - Input / output: <schema summary>
- **<handler recipe>** (Slack buttons, etc.):
  - Trigger: `slack_bot/bot_command_v2`
  - Flow: link via `complete_task`

### Connections
- **<connection>** (`<project>/Connections/<file>.connection.json`):
  - Provider: <provider>
  - Auth: <oauth2 / api_key / etc.>
  - Existing / new: <reuse or create>

### MCP / Genie (only if applicable)
- **<MCP server>**:
  - Skills: <list>
  - Purpose: <API-driven submission, etc.>

## Stage Transitions (when there is an approval flow, etc.)
<!-- Stage transition diagram. -->
```
draft → submitted → approved → completed
                 → rejected → (end)
```

## Resource Inventory
<!-- Resource info captured in Step 2. Flag anything that still has to be configured in the UI post-deploy. -->
- **Jira**: project `DEV`, issue type `Task`
- **Slack**: channel `#it-onboarding` (`C0123456`)
- **Google Sheets**: sheet `employees`, headers `[employee_id, manager_email, ...]`

## Unlearned Actions
<!-- Actions/triggers whose field info is not in docs and that you implemented best-effort. /tasks expands these into [learn] tasks. -->
| provider | action/trigger | notes |
|---|---|---|
| | | |

## Open Issues
<!-- Resource-fetch failures, items needing post-deploy verification, etc. -->
- <item>

## Decisions
<!-- Technical decisions and their reasons. -->
- <YYYY-MM-DD>: <decision> — <reason>
```

## Rules to follow

- **Do not work while spec Open Questions remain**: always finish `/clarify` first.
- **Do not skip the CATALOG / pattern lookup**: otherwise you miss reuse opportunities.
- **Always declare Unlearned Actions**: surface gaps now so the downstream `[learn]` task closes them.
- **Do not rewrite spec.md's body**: do not let technical terms leak back into spec. If the requirement needs changing, fix it on the requirements side via `/clarify`.

## Git management

```bash
git add projects/<project-name>/specs/<NNN>-<slug>/plan.md
git commit -m "plan(<project>/<slug>): initial workato design"
git push origin
```
