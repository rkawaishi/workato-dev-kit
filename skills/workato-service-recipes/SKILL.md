# Callable recipes by Workato recipes

Provider value to use in every step: `workato_service`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workato_service"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (0)

_None._


## Actions (4)

| Internal name | Title | Batch |
|---|---|---|
| `call_service` | Call recipe (synchronous) | - |
| `call_service_async` | Call recipe (asynchronous) | - |
| `send_reply` | Return response from recipe | - |
| `wait_for_async_jobs` | Wait for async calls | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `receive_request` | New call for recipe | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
