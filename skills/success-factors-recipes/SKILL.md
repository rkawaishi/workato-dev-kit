# SAP SuccessFactors OData recipes

Provider value to use in every step: `success_factors`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "success_factors"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_updated_object` | New or updated object | - |
| `new_updated_object_batch` | New or updated objects in batch | yes |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `advance_search_object` | Search records using OData query | yes |
| `create_object` | Create record | - |
| `get_object` | Get record details | - |
| `merge_object` | Merge record | - |
| `search_object` | Search records | yes |
| `update_object` | Update record | - |
| `upsert_object` | Upsert records (single object) | yes |
| `upsert_record_object` | Upsert record | - |
| `upsert_records_transactional` | Upsert records (multiple objects) | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
