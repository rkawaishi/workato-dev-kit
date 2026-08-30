# Workato EDI recipes

Provider value to use in every step: `workato_edi`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workato_edi"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_transactions_in_polling_bucket` | New transactions in bucket | - |


## Actions (6)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `convert_data_format` | Convert data format | - |
| `create_record` | Create record | - |
| `generate_label` | Generate label | - |
| `get_record` | Get record | - |
| `search_records` | Search records | yes |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `approve_delivery` | Approve delivery | - |
| `fail_delivery` | Fail delivery | - |
| `list_transactions_from_polling_bucket` | List transactions from polling bucket | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
