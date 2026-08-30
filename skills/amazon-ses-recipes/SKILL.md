# Amazon SES recipes

Provider value to use in every step: `amazon_ses`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "amazon_ses"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (0)

_None._


## Actions (8)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_object` | Create object | - |
| `delete_object` | Delete object | - |
| `get_object` | Get object | - |
| `list_object` | List object | yes |
| `send_bulk_email` | Send bulk email | yes |
| `send_email` | Send email | - |
| `update_object` | Update object | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
