---
description: Push local project changes to the Workato remote. Runs validation, pushes connections first, and guides the deploy end-to-end.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
disable-model-invocation: true
---

# /push-project

Push local changes to the Workato remote and verify the recipes work.

## Usage

- `/push-project` — push the current project
- `/push-project <project-name>` — switch to the specified project and push
- `/push-project --start` — start the recipes after pushing
- `/push-project --test` — start the recipes and verify job success after pushing
- `/push-project --restart-recipes` — auto-restart any running recipes after push (for updates)
- `/push-project --delete` — delete assets that exist remotely but not locally
- `/push-project --validate-only` — only validate (do not push)

## Procedure

### 1. Project validation

Validate the project's JSON files before pushing. With `--validate-only`, stop here.

#### 1a. JSON syntax check

Check the syntax of every JSON file under the project directory:

```bash
# Targets: *.recipe.json, *.connection.json, *.agentic_genie.json,
#          *.agentic_skill.json, *.mcp_server.json, *.lcap_app.json,
#          *.lcap_page.json, *.workato_db_table.json
for f in projects/<project-name>/*.json; do
  python3 -c "import json; json.load(open('$f'))" 2>&1 || echo "INVALID: $f"
done
```

Fix any errors before continuing.

#### 1b. `extended_output_schema` check

Confirm `extended_output_schema` is defined on these actions / triggers:

- **add_record / update_record / search_records**: field definitions for Data Table operations.
- **return_result**: result schema for Recipe Functions (required so datapills can be picked up by downstream steps).
- **Triggers in general**: especially `new_requests_realtime` should include Data Table fields in the schema.

```
# How to check: read the recipe JSON and verify extended_output_schema is present on each block.
# If missing, warn:
WARNING: step <keyword> in <recipe>.recipe.json is missing extended_output_schema.
  Datapills may not be visible in downstream steps.
```

#### 1c. Workflow App page component check

For `*.lcap_page.json`, check the `dataSource` on dropdown components:

```
# If dataSource is null, warn:
WARNING: dropdown "<label>" in <page>.lcap_page.json has dataSource: null.
  The selected value will not persist on push. Configure it in the UI or define dataSource in the JSON.
```

#### 1d. Workato CLI `recipes validate` (blocking)

**Inside Claude Code**: `kit/framework/claude/hooks/validate-before-push.sh` runs via the PreToolUse hook whenever it detects `workato push`. It runs `workato recipes validate --path <file>` on every `*.recipe.json`, catching format issues before push.

**Other editors (Cursor / Codex / Gemini)**: no auto-hook. Run `/validate-recipe` explicitly before push to verify the format.

- **Run time**: roughly 2 s per file (serial). On a large project, factor in the wait.
- **On failure**: print the error details and abort the push (exit 2).
- **Workspace constraint (warning only)**: if the workspace has an unreleased custom connector, the CLI's pre-check fails first and recipe-level validation never runs. In that case the warning "CLI validate skipped for N recipe(s): ... Release with 'workato sdk push' to enable deeper validation." appears, but push still proceeds. To enable deeper validation, release the custom connector with `workato sdk push`.

### 2. Detect new connections

Before pushing, inspect the `.connection.json` files in the project and detect any new connections that don't yet exist on the Workato remote.

How to detect:
- List the local `*.connection.json` files.
- Compare with the connections already retrieved by `workato pull` (i.e. existing on Workato).
- Identify newly created connection files.

### 3. Push (two-step or single-step)

**When there are new connections — two-step push:**

1. **Push only the connection files first**: either temporarily add the other files to `.workato-ignore`, or push from a directory containing only the connection files. **Never use `--delete`** here (it would delete existing remote assets).
2. Ask the user to authenticate:

```
Pushed new connections to Workato:
- <connection_name> (<provider>)

Authenticate them in the Workato UI:
1. Open the "<project>" project
2. Enter credentials for each connection

Tell me once authentication is done. I'll push the remaining assets next.
```

3. Once authentication is done, push every asset.

**No new connections — single-step push:**

```bash
workato projects use "<project-name>"
workato push
```

**With `--restart-recipes`:**

Use this when updating existing recipes and you need running recipes to auto-restart:

```bash
workato push --restart-recipes
```

This auto-restarts any running recipes after the push.
Use it to roll out logic changes, datapill fixes, or field additions to running recipes.
Not needed when pushing only new recipes.

**With `--delete`:**

Delete assets remotely that were removed locally:

```bash
workato push --delete
```

**Known limitation: the CLI's `--delete` cannot delete `agentic_skill` and `mcp_server`** (they show up as `Skipped`).
If you need to delete one, tell the user:

```
The CLI's --delete cannot remove MCP servers or skills (they end up Skipped).
Please delete the following in the Workato UI:
- <skills/mcp_server names to delete>

Re-push once they're removed.
```

### 4. Post-push deployment guidance

After a successful push, automatically display the relevant guidance based on the assets in the project.

#### Always shown: recipe start list

```
Push complete. Start the following recipes:
- <recipe_name_1>
- <recipe_name_2>

Open each recipe in the Workato UI and click "Start recipe",
or re-run /push-project with --start / --test.
```

#### When there are new connections

```
Verify authentication for these connections:
- <connection_name> (<provider>)

Enter credentials in Workato UI > project > Connections.
```

#### When there is an MCP server (`*.mcp_server.json`)

```
MCP server setup:
1. Open the MCP server configuration screen in the Workato UI.
2. Confirm the skill list shows under tools.
3. Review each tool's description.
4. Copy the MCP server URL and configure it in the AI client (Claude Desktop, etc.).
5. Test by calling the tool from the AI client.
```

#### When there is a Workflow App (`*.lcap_app.json`, `*.lcap_page.json`)

```
Workflow App UI verification checklist:
1. The Workflow App shows the stages and pages.
2. The submission form displays its fields correctly.
3. Dropdown options are populated.
4. The review page allows approve / reject.
5. Test: submit a request from the form and walk through the full approval flow.
```

### 5. Start recipes (`--start` / `--test`)

```bash
# List recipes in the project (folder_id comes from .workatoenv)
python3 scripts/workato-api.py recipes list --folder-id <folder_id>

# Start one recipe
workato recipes start --id <recipe-id>

# Start every recipe
workato recipes start --all
```

### 6. Job verification (`--test`)

```bash
# Failed jobs for a recipe
python3 scripts/workato-api.py jobs list --recipe-id <recipe-id> --status failed

# Job detail (error message)
python3 scripts/workato-api.py jobs get --recipe-id <recipe-id> --job-id <job-id>
```

### 7. Fix-error cycle

If a job fails:

1. Run `python3 scripts/workato-api.py jobs get` to read the error.
2. Diagnose:
   - **Datapill reference error**: wrong `path` → fix the recipe JSON.
   - **Connection not configured**: guide the user through connection auth in the UI.
   - **Field mapping error**: fix the field name / UUID in `input`.
   - **External API error**: ask the user to verify the connection target configuration.
3. Apply the fix and re-push.
4. Restart the recipe and verify the next job.
5. Repeat until success.

### 8. Report

- Push result.
- Validation warnings (if any).
- Recipe start status.
- Job success / failure (under `--test`).
- For any errors, the error content and suggested fixes.

## Notes

- Push overwrites the Workato remote.
- **Always push new connections first and authenticate them**: a recipe with an un-authenticated connection fails on push.
- For Workflow App triggers (`new_requests_realtime`, etc.), test by submitting the form.
- **`--delete` limitation**: `agentic_skill` and `mcp_server` cannot be deleted via CLI. Delete them manually in the UI.
- **`--restart-recipes`**: needed to roll out changes to running recipes. Not needed when pushing only new ones.

## Git management

**`/push-project` is a deploy to the Workato API; it has zero effect on git.** To also preserve local changes in your git remote, run git separately in the workspace repository:

```bash
git add projects/<project-name>/
git commit -m "<msg>"
git push origin
```

Do not assume "I ran /push-project, so the history is preserved."
