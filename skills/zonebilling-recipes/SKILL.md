# ZoneBilling for NetSuite recipes

Provider value to use in every step: `zonebilling`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "zonebilling"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (0)

_None._


## Actions (14)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_record` | Create Record | - |
| `create_records_batch` | Create Records | yes |
| `get_file` | Get File | - |
| `get_process_status` | Get Bulk API Status | yes |
| `get_record` | Get Record | - |
| `get_record_file` | Get Record File | - |
| `get_record_file_attachments` | Get Record File Attachments | - |
| `get_records` | Get Records | - |
| `post_automation` | Run ZAB Automation(s) | - |
| `update_record` | Update Record | - |
| `update_records_batch` | Update Records | yes |
| `upsert_record` | Upsert Record | - |
| `upsert_records_batch` | Upsert Records | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
