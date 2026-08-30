# PlanGrid recipes

Provider value to use in every step: `plan_grid`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "plan_grid"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_object` | New object in PlanGrid | - |
| `new_updated_object` | New or updated object in PlanGrid | - |


## Actions (7)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_object` | Create object | - |
| `download_object` | Download object | - |
| `get_object` | Get object by ID | - |
| `search_objects` | Search objects | yes |
| `update_object` | Update object | - |
| `upload_object` | Upload object | - |


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
