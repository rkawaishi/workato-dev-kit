# Deployment guide

Procedures for taking a Recipe or Workflow App from creation to running on Workato.
This guides the user step by step through the UI actions they need to perform after JSON generation.

## Recipe deployment flow

### Step 1: Push connections first (only when there are new connections)

When you create a new `.connection.json`, push the connection alone first and complete authentication.

```
Message to user:
---
A new connection has been created:
- <connection_name> (<provider>)

Pushing the connection to Workato. After the push, configure authentication in the UI:
1. Open the project in the Workato UI
2. Open the connection <connection_name>
3. Enter the credentials and click "Connect"
4. Confirm a successful connection

Let me know once authentication is complete. I will then push the Recipe.
---
```

**Why connection authentication must come first:**
- If you push a Recipe with an unauthenticated connection, field suggestions do not appear in the UI
- `extended_output_schema` is not expanded
- Test runs fail with errors

### Step 2: Push the Recipe

After connection authentication is complete (or when using an existing connection), push the Recipe.

```bash
workato push
```

### Step 3: Verify and adjust the Recipe in the UI

After the push, instruct the user to open the Recipe in the Workato UI and verify the following.

```
Message to user:
---
The Recipe has been pushed. Please verify the following in the Workato UI:

1. **Recipe structure**: Each step is displayed correctly
2. **Connection selection**: The correct connection is selected for each step
3. **Field mapping**: datapill references in input fields are correct
   - Warning: if a field is empty, reconfigure it in the UI
4. **Trigger configuration**: trigger-specific settings (table selection, event type, etc.)

If adjustments are needed, edit in the UI and let me know. I will pull and learn from it.
---
```

### Step 4: Pull and learn

When the user has made adjustments in the UI:
```bash
echo "y" | workato pull
```

After the pull, run `/learn-recipe` to extract and accumulate field information.

### Step 5: Test run

```
Message to user:
---
Please test-run the Recipe:
1. Click the "Test" button on the Recipe in the Workato UI
2. Enter test data and execute
3. Review the job results

If errors occur, let me know. I will analyze and fix them.
---
```

To check test results from the CLI:
```bash
workato recipes start --id <recipe-id>
python3 scripts/workato-api.py jobs list --recipe-id <recipe-id> --status failed
python3 scripts/workato-api.py jobs get --recipe-id <recipe-id> --job-id <job-id>
```

## Workflow App deployment flow

### Step 1: Enable the Workflow App (UI, one-time)

```
Message to user:
---
Please perform the following in the Workato UI:
1. Enable the Workflow App inside the project

Let me know once complete. I will then push the Data Table, stages, pages, and Recipes.
---
```

### Step 2: Push all assets

Push the Data Table, lcap_app, pages, and Recipes together.
If there are new connections, push the connection first as in Step 1 of the Recipe deployment flow.

### Step 3: UI verification

```
Message to user:
---
Push complete. Please verify the following in the Workato UI:
1. Stages and pages are reflected in the Workflow App
2. The submission form fields are displayed correctly
3. The review page allows approve/reject
4. Connection authentication (if using external services)
5. Field mapping for each step of the Recipe

Test: submit a request from the submission form and run through the full approval flow.
---
```

## MCP server deployment flow

### Step 1: Push

Push the MCP server, skills, and skill Recipes.

### Step 2: Enable the MCP server

```
Message to user:
---
Push complete. Please verify the MCP server in the Workato UI:
1. Open the MCP server settings screen
2. Confirm skills appear in the tool list
3. Confirm each tool's description is appropriate
4. Copy the MCP server URL and configure it in an AI client (Claude Desktop, etc.)

Test: invoke the tools from the AI client.
---
```

## Common errors and remedies

| Error | Cause | Remedy |
|---|---|---|
| `expired_access_token` | Connection not authenticated | Configure connection authentication in the UI |
| Empty field | UI cannot fetch schema because connection is not authenticated | After authenticating the connection, reconfigure the field in the UI |
| `Unresolved reference` | Referenced file does not exist | Push the referenced file first, or set the reference to null |
| Page editor stuck loading | Wrong component type (e.g. using input for a date type) | Fix to `type: "date"` |
| `parameters` reset to empty | Push reset fields where the connection was not configured | Authenticate connection, reconfigure in UI, then pull |
| datapill not recognized until reload | `return_result` lacks `extended_output_schema` / `extended_input_schema` | Expand the same field definitions as `result_schema_json` into the extended schemas |
| Trigger fields not recognized until refresh | Trigger lacks `extended_output_schema` | Expand the trigger output field definitions into `extended_output_schema`. In particular, include the Data Table fields in the schema of the Workflow App `new_requests_realtime` trigger |
| `PG::UniqueViolation` (agentic_skill) | Re-push while the skill already exists | The CLI `--delete` cannot remove MCP servers or skills (they show `Skipped`). Delete them manually in the UI, then re-push |
