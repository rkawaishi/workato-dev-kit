# Workato Genie recipes

Provider value to use in every step: `workato_genie`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workato_genie"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `start_workflow` | Start workflow | - |


## Actions (6)

| Internal name | Title | Batch |
|---|---|---|
| `assign_task_to_genie` | Assign task to genie | - |
| `create_request` | Create approval request | - |
| `create_task` | Assign task to user | - |
| `send_business_event` | Send business event | - |
| `upsert_knowledge` | Store knowledge | yes |
| `workflow_return_result` | Return response | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `update_kpi` | Update KPI | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
