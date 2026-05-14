# Shared asset design patterns

Decide on sharing case by case. Holding assets per project is often simpler, and over-sharing can make management more complex.

## When to consider sharing

When multiple projects reuse the same connection (e.g. Jira, Slack) or Recipe Function (e.g. fetch manager), centralized credential management or deduplication of logic may be needed.

## Workato's reference mechanism

Workato can **reference assets in a different project** via the `zip_name` and `folder` fields:

```json
"account_id": {
  "zip_name": "Shared/Connections/shared_jira.connection.json",
  "name": "Shared | Jira",
  "folder": "Shared"
}
```

- `folder`: name of the referenced project (use `""` within the same project)
- `zip_name`: path including the project name

## Recommended pattern: Shared project

### Project layout

```
projects/
├── Shared/                          # Project dedicated to shared assets
│   ├── Connections/
│   │   ├── shared_jira.connection.json
│   │   ├── shared_slack.connection.json
│   │   └── shared_gmail.connection.json
│   └── Recipes/
│       ├── fnc_get_line_manager.recipe.json
│       ├── fnc_get_department.recipe.json
│       └── fnc_send_notification.recipe.json
│
├── [App] PC Loan Request/           # Individual project
│   └── Recipes/
│       └── main_recipe.recipe.json  # -> references Shared connections / Functions
│
├── [App] Expense Reimbursement/     # Individual project
│   └── Recipes/
│       └── main_recipe.recipe.json  # -> references the same Shared assets
```

### Naming conventions

| Asset type | Naming | Example |
|---|---|---|
| Shared project | `Shared` | |
| Shared connection | `Shared \| <Provider>` | `Shared \| Jira`, `Shared \| Slack` |
| Shared Recipe Function | `fnc_<verb>_<noun>` | `fnc_get_line_manager`, `fnc_send_notification` |

### Referencing a connection

Reference a shared connection from a Recipe in an individual project:

```json
{
  "keyword": "application",
  "provider": "jira",
  "account_id": {
    "zip_name": "Shared/Connections/shared_jira.connection.json",
    "name": "Shared | Jira",
    "folder": "Shared"
  }
}
```

### Calling a Recipe Function

Call a shared Function from a Recipe in an individual project:

```json
{
  "provider": "workato_recipe_function",
  "name": "call_recipe",
  "input": {
    "flow_id": {
      "zip_name": "Shared/Recipes/fnc_get_line_manager.recipe.json",
      "name": "fnc: Get line manager",
      "folder": "Shared"
    },
    "parameters": {
      "requestor_email": "#{_dp('...')}"
    }
  }
}
```

## Recipe Function design guidelines

### Naming convention

```
fnc_<verb>_<noun>.recipe.json
```

| Pattern | Example | Purpose |
|---|---|---|
| `fnc_get_*` | `fnc_get_line_manager` | Data retrieval |
| `fnc_send_*` | `fnc_send_slack_notification` | Send notifications |
| `fnc_validate_*` | `fnc_validate_budget` | Validation |
| `fnc_create_*` | `fnc_create_jira_ticket` | Create records in external systems |
| `fnc_update_*` | `fnc_update_employee_status` | Update records in external systems |

### Interface design

Define clear inputs and outputs for shared Functions:

```json
{
  "provider": "workato_recipe_function",
  "name": "execute",
  "input": {
    "parameters_schema_json": "[{schema of input parameters}]",
    "result_schema_json": "[{schema of output parameters}]"
  }
}
```

- **Keep inputs minimal**: accept only the parameters you need (1-3 is ideal)
- **Make outputs explicit**: return all fields the caller needs
- **Error handling**: try/catch inside the Function; report errors via an `error` field

### Example: fnc_get_line_manager

```
Input: requestor_email (string)
Output: manager_name (string), manager_email (string)
```

### Example: fnc_send_slack_notification

```
Input: channel (string), message (string), thread_ts (string, optional)
Output: ok (boolean), ts (string)
```

## Shared vs. individual decision

Whether to share or keep separate depends on the **nature and purpose of the asset**, not on usage count.

### Cases that should stay individual

| Situation | Reason |
|---|---|
| Connections for agents | Dedicated permissions / scopes are preferable. Sharing with other Recipes risks over-permissioning |
| Logic confined to a specific flow | It is only meaningful in that project's context |
| Different scope / authentication required | Even for the same service, split connections per purpose |

### Cases that benefit from sharing

| Situation | Reason |
|---|---|
| Cross-organization common logic | Manager lookup, department fetch, etc. return the same result for every project |
| Infrastructure-level connections | Company-wide Slack workspace, shared Jira project, etc. |

## Cautions

- Changing an asset in the Shared project affects every project that references it
- If the authentication of a Shared connection changes, every reference must be retested
- When running `workato push --delete` against the Shared project, be careful not to break references from other projects
- When changing the input/output of a Recipe Function, verify compatibility with every caller
