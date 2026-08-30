# Apttus Intelligent Cloud recipes

Provider value to use in every step: `apttus_intelligent_cloud`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "apttus_intelligent_cloud"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_object` | New object | - |
| `new_or_updated_object` | New or updated object | - |


## Actions (3)

| Internal name | Title | Batch |
|---|---|---|
| `create_object` | Create object | - |
| `search_object` | Search object | yes |
| `update_object` | Update object | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
