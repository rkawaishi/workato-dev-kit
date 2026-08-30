# OutSystems recipes

Provider value to use in every step: `out_systems`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "out_systems"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `new_record` | New record | - |
| `new_record_batch` | New record | yes |
| `new_updated_record` | New/updated record | - |
| `new_updated_record_batch` | New/updated record | yes |


## Actions (6)

| Internal name | Title | Batch |
|---|---|---|
| `create_batch_record` | Create records | yes |
| `create_record` | Create record | - |
| `get_entity_by_id` | Get entity by ID | - |
| `search_records` | Search records | yes |
| `update_batch_record` | Update records | yes |
| `update_record` | Update record | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
