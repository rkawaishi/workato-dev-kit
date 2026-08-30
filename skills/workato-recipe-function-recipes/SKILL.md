# Recipe function by Workato recipes

Provider value to use in every step: `workato_recipe_function`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workato_recipe_function"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `execute` | New call for function | - |


## Actions (4)

| Internal name | Title | Batch |
|---|---|---|
| `call_recipe` | Call a recipe function (synchronous) | - |
| `call_recipe_async` | Call a recipe function (asynchronous) | - |
| `return_result` | Return data from a recipe function | - |
| `wait_for_async_jobs` | Wait for async calls | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
