# Deployment guide

Steps and troubleshooting for deploying locally built assets to Workato.

The same skills and the same flow apply whether you use Claude Code or Cursor.

## Basic flow

All deployments go through the `/push-project` skill. You should not need to run `workato push` manually.

```
/push-project                     # Standard push (with validation)
/push-project --start             # Auto-start Recipes after push
/push-project --test              # Test-run after push and check results
/push-project --delete            # Also remove unused remote assets
```

## Deploying Recipes

### New Recipes (with new connections)

When new connections are involved, a **two-stage push** is required.

```
Step 1: /push-project
  → Pushes connections only first
  → You will be prompted: "Please authenticate the connection in the Workato UI"

Step 2: Authenticate the connection in the UI
  → Enter credentials and run a connection test

Step 3: /push-project --start
  → Push the remaining assets (Recipes, etc.)
  → Start the Recipes
```

**Why two stages:** if a connection is unauthenticated, the `pick_list` fields (dynamic dropdowns) inside the Recipe cannot resolve, and the push will fail.

### Updating existing Recipes

```
/push-project --restart-recipes
```

When updating a running Recipe, `--restart-recipes` automatically stops, updates, and restarts it.

### Test runs

```
/push-project --test
```

After pushing, the Recipe is test-run and the job's success/failure is checked. On failure, job details are retrieved for error analysis.

## Deploying Workflow Apps

Workflow App is the only case that requires UI enablement.

```
Step 1: Workato UI → Settings → Workflow Apps → enable

Step 2: /push-project
  → Pushes Data Table, app definition, pages, and Recipes together

Step 3: Verify in the UI
  → Test page rendering, stage transitions, and data entry
```

**Deployment order:** Data Table → lcap_app.json → Pages → Recipes. `/push-project` resolves the dependencies automatically.

## Deploying Genie / MCP server

```
Step 1: /push-project
  → Pushes Genie definition, skill definition, MCP server definition, and skill Recipes

Step 2: Verify in the UI
  → Confirm the skill is recognized in Agent Studio
  → For MCP servers, confirm the tools are discoverable

Step 3: Test
  → Invoke the skill from Genie chat and confirm it behaves as expected
```

**Note:** `/push-project --delete` cannot remove `agentic_skill` or `mcp_server` (CLI limitation). Remove these manually from the UI.

## Deploying custom connectors

Push custom connectors via the API helper (authenticates with the Platform CLI profile):

```bash
# Upload to Workato
python3 scripts/workato-api.py sdk push --connector connectors/<name>/connector.rb --title "<Title>"

# Update an existing connector
python3 scripts/workato-api.py sdk push --connector connectors/<name>/connector.rb --connector-id <id>

# Local test (Ruby gem CLI)
cd connectors/<name>
bundle exec workato exec connector.rb test
```

## Pre-push validation

`/push-project` automatically runs the following checks:

| Check | Target | Description |
|---|---|---|
| JSON syntax | All `.json` files | Whether they parse |
| Required fields | `.recipe.json` | Presence of `name`, `code`, `config` |
| extended_output_schema | Action steps | Presence of field definitions referenced by downstream steps |
| Page components | `.page.json` | Consistency of `dataSource` definitions |
| UUID format | Recipe steps | Format check on `uuid` fields |

To run validation only, use `/validate-recipe`.

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `Connection not found` | Connection is unpushed or unauthenticated | Use the two-stage push and authenticate the connection first |
| `Token expired` | API token has expired | Re-authenticate with `workato init` |
| `Unresolved reference` | The referenced asset does not exist | Push the dependency first |
| `Schema validation error` | JSON structure does not match the spec | Check details with `/validate-recipe` |
| `Recipe is running` | Updating a running Recipe | Use the `--restart-recipes` option |
| `pick_list resolution failed` | Dynamic dropdowns cannot resolve because the connection is unauthenticated | Authenticate the connection in the UI, then push again |
| `Skipped: agentic_skill` | CLI does not support deleting skill/MCP | Delete manually from the UI |

## Post-deployment learning cycle

If you adjust things in the UI after deploying, always run the pull → learn cycle:

```
/pull-project                     # Pull UI changes back to local
/learn-recipe <project>    # Learn new insights from the changes
```

This accumulates field values that can only be set in the UI, as well as undocumented structures, into the knowledge base.
