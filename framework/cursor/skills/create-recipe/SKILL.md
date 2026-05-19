---
name: create-recipe
description: Generate Workato recipe JSON interactively. Pick a provider, trigger, and actions to produce a .recipe.json and a .connection.json. Japanese prompts are also supported.
---

# /create-recipe

Generates Workato recipe JSON files. In the spec-driven workflow (`/spec` → `/plan` → `/tasks` → `/implement`), this skill is invoked from `[recipe]` / `[function]` / `[handler]` tasks.

## Usage

- `/create-recipe <project>/<NNN>-<slug>` — pull context from `plan.md` and generate (**preferred**; this is how `/implement` invokes it automatically)
- `/create-recipe <project>` — only the project is fixed; if a `plan.md` exists we look it up and confirm with the user
- `/create-recipe` — infer from context; confirm `<project>/<NNN>-<slug>`

> **Note**: as part of the migration to the spec-driven workflow, the legacy `DESIGN.md` reference is retired. Start new projects with `/spec`; for existing projects, run `/design migrate` first to convert into `specs/`.

## Procedure

### 0. Pull context from plan.md

When `<project>/<NNN>-<slug>` is supplied (or can be inferred), read `projects/<project>/specs/<NNN>-<slug>/plan.md` and take the following as **defaults**:

| plan.md section | What to pull in |
|---|---|
| `## New Components` `### Recipes` | The target recipe definition (trigger, flow, inputs/outputs) |
| `## New Components` `### Connections` | Connections to use (provider, auth method) |
| `## Reused Assets` | Shared Functions / Connections to reference via `call_recipe` |
| `## Resource Inventory` | Resource values (Slack channel, Jira project, etc.) — no interview needed |
| `## Applied Patterns` | Construction patterns (step-composition guidance) |
| `## Unlearned Actions` | Best-effort-implementation flag |

If plan.md does not exist or cannot be read, fall back to the interactive interview mode (continue to Step 1).

### 1. Interview the recipe design

Confirm with the user:
- **Recipe purpose**: what you want to automate.
- **Trigger**: which app's which event starts the recipe (e.g. "new email in Gmail").
- **Actions**: what happens after the trigger (e.g. "upload file to Google Drive").
- **Conditions**: any filter conditions.
- **Target project**: which project directory the file goes into.

### 2. Check the shared asset catalog

If `projects/CATALOG.md` exists, read it. Look for existing assets matching the requirements:
- **Connections**: if a shared connection for the same provider exists → propose reusing it.
- **Recipe Functions**: if the logic you need (manager lookup, notification sender, etc.) already exists → propose calling it via `call_recipe`.
- If you find matching assets, propose them to the user and bake them in only after they approve.

If the catalog is missing, skip this and tell the user it can be generated with `/catalog scan`.

### 3. Check the connector knowledge

- Use `docs/connectors/_index.md` to identify the connector you'll use.
- Read `docs/connectors/<connector>.md` for available triggers/actions and field info.

### 4. Verify field details

- If the connector doc has an Input/Output fields section for the target action, use it.
- **If the field info is missing**: fetch the official docs with WebFetch.
  - URL pattern: `https://docs.workato.com/en/connectors/<name>/<action-name>.html`
  - Or: `https://docs.workato.com/en/connectors/<name>/actions.html`
- Append what you fetched to `docs/connectors/<connector>.md` so the knowledge accumulates.
- **Prohibited**: do not grep `projects/<other-project>/Recipes/` to copy fields from sample JSON. That leaks project-specific logic and naming, and it hides documentation gaps (see "Recipe implementation lifecycle" in `@.claude/CLAUDE.md`).
- If you have to implement best-effort because there's no documentation anywhere, append `provider` / `action` to the `## Unlearned Actions` table in `projects/<project>/specs/<NNN>-<slug>/plan.md`. If possible, add a matching `[learn]` task to the same directory's `tasks.md` (or regenerate via `/tasks --update`).

### 5. Auto-fetch resource info

For each provider used by the recipe, pull resource information through an MCP server or CLI tool.

#### Procedure

1. **Load the environment config**: read `.resource-providers.yml`. If it doesn't exist, either walk the user through the initial setup or skip to Step 6 (see "Initial setup" in `docs/platform/resource-providers.md`).
2. **Match providers**: check whether the providers chosen in Step 1 are defined in `.resource-providers.yml`.
3. **Detect and run tools**: for each defined provider, detect and run the tool following "How skills use this" in `docs/platform/resource-providers.md`.
4. **Present choices**: surface the retrieved info to the user as multiple-choice.
   ```
   Fetched the Jira project list:
   1. DEV - Development
   2. OPS - Operations
   Which project should the ticket land in?
   ```
5. **Fallback**: in any of the failure modes (no config file, undefined provider, tool detection failure, fetch error), silently skip and fall back to the normal interview in Step 6.

> **Important**: never block on a fetch failure. Do not show error messages — transition naturally to the interview flow.

### 6. Decide and interview input values (important)

Classify each step's `input` fields by how the value is decided:

#### A. Auto-decidable values (no interview needed)
- **Datapill references**: values that reference an earlier step's output.
  - e.g. putting a Slack message's text into Jira's description.
- **Fixed values**: values uniquely determined by the recipe logic.
  - e.g. `"type": "expense"`, `"status": "active"`.
- **Auto-fetched in Step 5**: values the user already picked (project keys, channel IDs, etc.).

#### B. Values that need user confirmation
These cannot be decided from the recipe logic alone. **Interview the user before generating JSON.**
Skip values that were already picked in Step 5.

| Category | Examples | Sample question |
|---|---|---|
| **Send / post target** | Slack channel name / ID, email recipient | "Which channel should we post to?" |
| **Project / space** | Jira project, Confluence space | "Which Jira project should the ticket land in?" |
| **Category / type selection** | Jira issue type, priority | "Issue type — Task, Bug, or Story?" |
| **Data source specifics** | Google Sheets sheet name, DB table name | "Which sheet are we searching?" |
| **Templates / formats** | Message template, subject line format | "What format should the message use?" |
| **Thresholds / conditions** | Filter threshold, day count | "Tickets from how many days back?" |
| **Auth / endpoint specifics** | API endpoint, database name | "Which environment is the connection target?" |

> **Note**: even when input field info is missing from the docs, data-source-style actions (search, fetch, etc.) always need a target resource (sheet name, table name, project name, etc.). Even if the field details are unclear, ask "What does this action target?".

#### C. Values that are decided only after the connection is configured
- Salesforce object types, custom fields, etc. — dynamically retrieved after the connection is configured.
- Leave these out: set `input: {}` and configure them in the UI after deploy.

#### How to run the interview

1. Enumerate the input fields of every step.
2. Classify each as A/B/C (values already picked in Step 5 count as A).
3. Ask the user about every B at once (not one field at a time).
4. Once you have the answers, proceed to JSON generation.

Sample (without auto-fetch):
```
Before I generate the recipe, let me confirm a few values:

1. **Slack channel for posting**: which channel should the notifications go to? (e.g. #general, #it-helpdesk)
2. **Jira project**: which project should the ticket be created in? (e.g. IT, HELPDESK)
3. **Jira issue type**: which issue type? (e.g. Task, Bug, Story)
4. **Approval deadline**: how many days for the approval task? (default: 7)
```

Sample (with auto-fetch):
```
I retrieved resource info from the Slack and Jira MCPs.

**Slack channels** — pick a post target:
1. #general (C01234567)
2. #it-helpdesk (C07654321)
3. #dev-notifications (C09876543)

**Jira project DEV** issue types: Bug, Story, Task, Epic
→ Which issue type?

Remaining items:
- **Approval deadline**: how many days for the approval task? (default: 7)
```

### Steps 7–9 — recipe JSON generation

Steps 7–9 below are the **JSON generation procedure**. Generating a recipe produces ~1000 lines of JSON; running it inline keeps that JSON in the main conversation for the rest of the session even though it is never read again.

- **In Claude Code**: dispatch Steps 7–9 to the **`workato-builder` subagent** rather than running them in the main conversation. Spawn it with the `Agent` tool (`subagent_type: workato-builder`) and pass asset type `recipe` plus the design from Steps 0–6 — the interview results (or the `plan.md` pointer), the catalog / pattern findings, the interviewed input values, and the target file paths. The subagent runs on Sonnet, executes Steps 7–9, validates and writes the files, and returns a short summary; the large JSON never enters the main context. Continue at "Output and deployment guide" using that summary.
- **In editors without subagent support** (Cursor / Codex / Gemini): perform Steps 7–9 inline.

The generation procedure itself is the same either way:

### 7. Read the JSON structure reference

- `.cursor/rules/workato-recipe-format.mdc`
- If logic steps are needed, read the relevant file under `docs/logic/`.

### 8. Design the step composition (apply patterns)

Use the interview results to design the step composition. As you do, look for patterns in the catalog that apply.

1. Read the pattern catalog (kit and org sides; org wins on conflicts):
   - `docs/patterns/recipe-patterns/_index.md` — kit canonical patterns
   - `org/docs/patterns/recipe-patterns/_index.md` — org-recorded patterns (if present)
   - `projects/docs/patterns/` — legacy patterns (read-only for backwards compatibility)
2. Decompose the interview's requirements and find a pattern for each piece:
   - e.g. "fetch everything from an API and sync into a DB" → **pagination loop** + **data sync**
   - e.g. "submit → approve → create Jira" → **approval workflow**
   - A pattern can apply to **the whole recipe** or to **just a few steps**.
3. Read the matching pattern files; pull in their step composition, decision points, and known caveats.
4. When combining multiple patterns, decide the order in which they appear in the recipe.

For parts that don't match a pattern, consult:
- `docs/logic/data-pills.md` for datapill notation.
- The relevant file under `docs/logic/` for the syntax of any logic step.
- `docs/patterns/deployment-guide.md` for deploy-time caveats.
- Existing recipes in the same project, when applicable.

### 9. Generate the files

Follow `.cursor/rules/workato-project-structure.mdc`:
- `<project>/Recipes/<snake_case_name>.recipe.json` — the recipe.
- `<project>/Connections/<prefix>_<provider>.connection.json` — connection (only if it doesn't exist yet).
- Make sure `zip_name` / `folder` inside the JSON match the subfolder path.

## Generation rules

- `number` starts at 0 for the trigger; subsequent steps are 1, 2, 3, ...
- Generate a UUID (v4) for every step.
- `as` is the step's reference name. Outside Genie workflows, use the same value as `name`.
- For Genie workflows, use a random 8-character hex string for `as`.
- The `config` array must include connection references for every provider in use.
- `version` is 1 for a new recipe.
- `private` is true.
- `concurrency` is 1 (default).

## Setting input fields

- **A (auto)**: fill with a datapill or a fixed value.
- **B (interviewed)**: use the value from Step 6.
- **C (connection-dependent)**: leave out of `input` (configure in the UI after deploy).

When field info is missing from the docs, push with `input: {}`, then configure in the UI and pull to learn.

## Generating datapills

To reference another step's output in an input field:
```
#{_dp('{"pill_type":"output","provider":"<provider>","line":"<as>","path":["<field>"]}')}
```

- `provider` and `line` come from the source step.
- `path` is an array of field names (nested = multiple elements).
- **Look up each `path` value in the connector docs' Output fields — get it exactly right.**

## Output and deployment guide

After generation, display:
- The list of generated files.
- A structural summary of the recipe (trigger → action flow).
- A summary of the values you filled in from the interview.
- Any fields you left empty for C (connection-dependent), explicitly called out.

Then, following "Recipe deployment flow" in `docs/patterns/deployment-guide.md`, walk through the deploy in stages:

1. **Push**: `workato push` to push every asset.
2. **After push, share the project URL**: build it from `.workatoenv`'s `folder_id` + the region.
3. **For new connections**: guide the user through connection auth **before** the recipe review.
   ```
   First, authenticate the connection:
   - <connection_name> (<provider>)
   Let me know when authentication is done.
   ```
4. **After auth, guide UI verification**: recipe structure, field mappings.
5. **Learning (mandatory)**: pull → `/learn-recipe`. **Do not skip** if you used any action recorded in `projects/<project>/specs/<NNN>-<slug>/plan.md`'s `## Unlearned Actions` or the same directory's `tasks.md` `[learn]` tasks (otherwise documentation gaps stay open). Once learning is done, close out the entry / task.
6. **Test run**: test in the UI; analyze and fix errors if any.
7. **Pattern accumulation**: if the recipe contains a new construction pattern, add it to the catalog via `/learn-pattern`.

## Git management

Generated files (`Recipes/`, `Connections/`) live under `projects/<project-name>/`. Commit them in the workspace repository:

```bash
git add projects/<project-name>/Recipes/ projects/<project-name>/Connections/
git commit -m "Add recipe: <name>"
git push origin
```

`workato push` is the deploy to the Workato API, separate from git.
