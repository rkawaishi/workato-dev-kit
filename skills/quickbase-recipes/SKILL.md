# Quickbase recipes

Provider value to use in every step: `quickbase`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "quickbase"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (5)

| Internal name | Title | Batch |
|---|---|---|
| `new_record` | New record | - |
| `new_record_webhook_trigger` | New record | - |
| `scheduled_table_query` | Scheduled record search using query | yes |
| `updated_record` | New/updated record | - |
| `updated_record_webhook_trigger` | New/updated record | - |


## Actions (9)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_record` | Create record | - |
| `bulk_upsert_records` | Create and update records in bulk from CSV file | yes |
| `delete_record` | Delete record | - |
| `download_attachment` | Download attachment | - |
| `edit_record` | Update record | - |
| `get_records_from_a_report` | Get records from report in Quickbase | yes |
| `purge_records_by_query` | Delete records in a report | yes |
| `search_records` | Search records | yes |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_form_entry` | New record | - |
| `new_record_webhook` | New record | - |
| `updated_form_entry` | Updated record | - |
| `updated_record_webhook` | New/updated record | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `search_record` | Search record | - |
| `update_record` | Update record | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
