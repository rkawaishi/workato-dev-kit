# JumpCloud recipes

Provider value to use in every step: `jump_cloud`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "jump_cloud"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_object` | New object | - |


## Actions (16)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_association` | Create association | - |
| `create_object` | Create object | - |
| `delete_association` | Delete association | - |
| `delete_object` | Delete object | - |
| `get_object_by_id` | Get object by ID | - |
| `list_objects` | List objects | yes |
| `list_objects_by_id` | List objects by ID | yes |
| `lock_user` | Lock user | - |
| `reset_user_mfa` | Reset user mfa | - |
| `run_trigger_command` | Run trigger command | - |
| `search_objects` | Search objects | yes |
| `search_user_by_employee_id` | Search user by employee ID | - |
| `unlock_user` | Unlock user | - |
| `update_object` | Update object | - |
| `update_user_on_system` | Update user on system | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `custom_action` | Custom action | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
