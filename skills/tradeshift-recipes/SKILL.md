# Tradeshift recipes

Provider value to use in every step: `tradeshift`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "tradeshift"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `credit_note_ready` | Credit note ready | - |
| `invoice_ready` | Invoice ready | - |


## Actions (11)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_code` | Create chart of accounts | - |
| `create_credit_note` | Create Credit note | - |
| `create_external_connection` | Create external connection | - |
| `create_invoice` | Create Invoice | - |
| `delete_coding_list` | Delete chart of accounts | - |
| `get_account_info` | Get current account info | - |
| `search_connections` | Search connections | yes |
| `tag_document` | Tag document | - |
| `untag_document` | Untag document | - |
| `update_connection_properties` | Update connection properties | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
