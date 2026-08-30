# SAP OData recipes

Provider value to use in every step: `sap_s4_hana_cloud`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "sap_s4_hana_cloud"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_object` | New object | - |
| `new_or_updated_object` | Updated object | - |


## Actions (9)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `batch_request` | Batch request | yes |
| `create_object` | Create object | - |
| `delete_object` | Delete object | - |
| `get_object` | Get object details by ID | - |
| `search_object` | Search object | yes |
| `search_object_with_proxy` | Extract bulk data | - |
| `update_object` | Update object | - |
| `upsert_object` | Upsert object | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
