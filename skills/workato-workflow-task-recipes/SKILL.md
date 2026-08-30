# Workflow apps by Workato recipes

Provider value to use in every step: `workato_workflow_task`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workato_workflow_task"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (5)

| Internal name | Title | Batch |
|---|---|---|
| `app_function_generic_request` | New component event | - |
| `app_function_load_dropdown_request` | New component event (Dropdown) | - |
| `app_function_load_table_request` | New component event (Table widget) | - |
| `new_requests_realtime` | New request | - |
| `updated_requests_realtime` | New/updated request | - |


## Actions (15)

| Internal name | Title | Batch |
|---|---|---|
| `add_request` | Create request | - |
| `app_function_return` | Return data to component | - |
| `change_workflow_stage` | Change workflow stage | - |
| `complete_task` | Complete workflow task programmatically | - |
| `delete_request` | Delete request | - |
| `delete_user` | Remove user | - |
| `find_users` | Get user data | yes |
| `get_requests` | Search requests | yes |
| `human_review_on_existing_record` | Assign task to users | - |
| `invite_user` | Invite user | - |
| `list_workflow_stages` | List workflow stages | - |
| `lookup_events` | Get activity history | yes |
| `share_request` | Share request | - |
| `unshare_request` | Unshare request | - |
| `update_request` | Update request | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `app_function_load_dropdown_return` | Return data to component | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
