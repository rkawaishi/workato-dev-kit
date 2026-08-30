# AWS Lambda recipes

Provider value to use in every step: `aws_lambda`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "aws_lambda"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_function` | New function created | - |


## Actions (3)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `get_function_by_name` | Get function details | - |
| `invoke_function` | Invoke function | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
