# Librato recipes

Provider value to use in every step: `librato`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "librato"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `triggered_alerts` | Triggered alerts | - |


## Actions (4)

| Internal name | Title | Batch |
|---|---|---|
| `get_alert_by_id` | Get alert by ID | - |
| `search_alerts` | Search alerts | yes |
| `search_metrics` | Search metrics | yes |
| `update_alert` | Update alert | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
