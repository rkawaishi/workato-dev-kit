# Azure Blob Storage recipes

Provider value to use in every step: `azure_blob_storage`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "azure_blob_storage"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_blob` | New blob | - |
| `new_event_webhook` | New event | - |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_container` | Create container | - |
| `download_blob` | Download blob contents | - |
| `generate_presigned_url` | Generate pre-signed URL | - |
| `get_blob_properties` | Get blob properties | - |
| `get_container_properties` | Get container properties | - |
| `search_blob` | Search blobs | yes |
| `search_container` | Search containers | yes |
| `update_blob_metadata` | Update blob metadata | - |
| `upload_blob` | Upload blob | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
