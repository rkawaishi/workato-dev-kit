# Scheduler by Workato recipes

Provider value to use in every step: `clock`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "clock"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `scheduled_event` | New recurring event | - |


## Actions (3)

| Internal name | Title | Batch |
|---|---|---|
| `get_time` | Get current time | - |
| `wait_for_interval` | Wait for time duration | - |
| `wait_until_time` | Wait until specified time | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `daily_task` | New scheduled event (advanced) | - |
| `timer` | New scheduled event | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `pause` | Wait | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
