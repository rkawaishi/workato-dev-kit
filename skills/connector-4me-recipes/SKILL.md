# 4me recipes

Provider value to use in every step: `connector_4me`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "connector_4me"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_event` | Webhook event | - |


## Actions (4)

| Internal name | Title | Batch |
|---|---|---|
| `custom_operation` | Custom action | - |
| `mutation` | Mutate records | - |
| `query` | Query records | - |
| `upload_attachment` | Upload attachment | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
