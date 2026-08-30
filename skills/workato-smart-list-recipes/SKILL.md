# SQL Collection by Workato recipes

Provider value to use in every step: `workato_smart_list`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workato_smart_list"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (0)

_None._


## Actions (5)

| Internal name | Title | Batch |
|---|---|---|
| `create_list` | Create list | yes |
| `create_list_from_csv` | Create list from CSV file | yes |
| `insert_rows` | Insert rows | yes |
| `insert_rows_from_csv` | Insert rows from CSV file | yes |
| `query_list` | Query lists | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
