# Google Workspace recipes

Provider value to use in every step: `google_workspace`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "google_workspace"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `new_admin_activity_event` | New admin activity event | - |
| `new_application_activity_event` | New application activity event | - |
| `new_user_event` | New user event | - |


## Actions (8)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_object` | Add record | - |
| `delete_object` | Delete record | - |
| `get_object` | Get record | - |
| `mobile_device_action` | Mobile device action | - |
| `search_object` | Search records | yes |
| `transfer_data_v2` | Transfer Data | - |
| `update_object` | Update record | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `transfer_data` | Transfer data | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
