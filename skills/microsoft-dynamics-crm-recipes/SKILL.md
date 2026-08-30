# Microsoft Dynamics 365 recipes

Provider value to use in every step: `microsoft_dynamics_crm`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "microsoft_dynamics_crm"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (11)

| Internal name | Title | Batch |
|---|---|---|
| `created_bulk_object` | Export new records | - |
| `created_or_updated_bulk_object` | Export new/updated records | - |
| `deleted_object` | Deleted object | - |
| `monitor_changes_delta_link_trigger` | Monitor changes in entities | - |
| `monitor_changes_delta_link_trigger_batch` | Monitor changes in entities | yes |
| `new_object_v2` | New object | - |
| `new_or_updated_batch_object` | New or updated object (batch) | yes |
| `new_or_updated_object_v2` | New or updated object | - |
| `new_webhook` | New object | - |
| `scheduled_object_search` | Scheduled object search | yes |
| `updated_webhook` | New/updated object | - |


## Actions (9)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `close_case` | Close case | - |
| `create_object` | Create object | - |
| `create_object_batch` | Create object | yes |
| `get_object_by_id` | Get object by ID | - |
| `get_object_schema` | Get object schema | - |
| `search_objects` | Search objects | yes |
| `update_object` | Update object | - |
| `update_object_batch` | Update object | yes |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_object` | New object | - |
| `new_or_updated_object` | New or updated object | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
