# NetSuite REST recipes

Provider value to use in every step: `netsuite_rest`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "netsuite_rest"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (0)

_None._


## Actions (14)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_record` | Create a record | - |
| `create_record_async` | Create records (async) | yes |
| `delete_record` | Delete a record | - |
| `delete_record_async` | Delete records (async) | yes |
| `execute_restlet` | Execute RESTlet script | - |
| `execute_suiteql` | Execute SuiteQL query | yes |
| `get_job_result` | Get async job result | - |
| `get_record` | Get a record by ID | - |
| `search_records` | Search records | yes |
| `update_record` | Update a record | - |
| `update_record_async` | Update records (async) | yes |
| `upsert_record` | Upsert a record | - |
| `upsert_record_async` | Upsert records (async) | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
