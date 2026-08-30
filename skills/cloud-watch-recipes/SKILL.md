# Cloud Watch recipes

Provider value to use in every step: `cloud_watch`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "cloud_watch"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_or_updated_alarm` | New or updated alarm | - |


## Actions (3)

| Internal name | Title | Batch |
|---|---|---|
| `disable_alarm` | Disable alarm | - |
| `enable_alarm` | Enable alarm | - |
| `set_alarm_state` | Set alarm state | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
