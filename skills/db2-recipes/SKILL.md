# IBM Db2 recipes

Provider value to use in every step: `db2`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "db2"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (0)

_None._


## Actions (7)

| Internal name | Title | Batch |
|---|---|---|
| `delete_rows` | Delete rows | yes |
| `export_csv_v2` | Export query result | - |
| `insert_rows_batch` | Insert rows | yes |
| `run_custom_sql` | Run custom SQL | yes |
| `search_rows` | Select rows | yes |
| `search_rows_sql` | Select rows using custom SQL | yes |
| `upsert_rows_batch` | Upsert rows | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
