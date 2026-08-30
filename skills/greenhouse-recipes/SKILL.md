# Greenhouse recipes

Provider value to use in every step: `greenhouse`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "greenhouse"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `new_event` | New event | - |
| `new_object_v3` | New object (v3) | - |
| `new_or_updated_objects_batch_v3` | New/updated object (v3) | yes |


## Actions (8)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_attachment_v3` | Create attachment (v3) | - |
| `create_object_v3_post` | Create object (v3) | - |
| `mark_candidate_hire_v3` | Mark candidate as hired (v3) | - |
| `move_application_v3` | Move application (v3) | - |
| `reject_application_v3` | Reject application (v3) | - |
| `search_object_v3` | Search objects (v3) | yes |
| `update_object_v3_patch` | Update object (v3) | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_object` | New object | - |
| `new_or_updated_objects_batch` | New/updated object | yes |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `advance_application` | Advance application | - |
| `create_object` | Create object | - |
| `get_object` | Get object by ID | - |
| `mark_candidate_hire` | Mark candidate as hired | - |
| `reject_application` | Reject application | - |
| `search_object` | Search object | yes |
| `update_object` | Update object | - |
| `upload_attachment` | Upload attachment | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
