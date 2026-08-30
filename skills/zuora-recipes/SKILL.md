# Zuora recipes

Provider value to use in every step: `zuora`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "zuora"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_updated_order` | New/updated order | - |
| `new_updated_record` | New/updated record | - |


## Actions (12)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_custom_object` | Create custom record | yes |
| `create_record` | Create record | - |
| `get_custom_object_record` | Get custom record | - |
| `get_object` | Get record | - |
| `get_order` | Get order by order number | yes |
| `get_subscriptions` | Get orders by subscription number | - |
| `query_records` | Query records | yes |
| `search_records` | Search records | yes |
| `update_custom_object` | Update custom record | yes |
| `update_order_triggerdate` | Update order trigger date | - |
| `update_record` | Update record | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
