# ParseHub recipes

Provider value to use in every step: `parsehub`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "parsehub"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (0)

_None._


## Actions (3)

| Internal name | Title | Batch |
|---|---|---|
| `cancel_a_run` | Cancel a run | - |
| `get_data_for_a_run` | Get data for a run | - |
| `start_a_run` | Start a run | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
