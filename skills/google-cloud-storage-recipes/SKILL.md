# Google Cloud Storage recipes

Provider value to use in every step: `google_cloud_storage`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "google_cloud_storage"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (0)

_None._


## Actions (12)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_bucket` | Create bucket | - |
| `delete_bucket` | Delete bucket | - |
| `delete_object` | Delete Object | - |
| `download_object` | Download object | - |
| `get_bucket` | Get bucket | - |
| `get_object_metadata` | Get object metadata | - |
| `list_buckets` | List buckets | yes |
| `list_objects` | List Objects | yes |
| `update_bucket` | Update bucket | - |
| `update_object_metadata` | Update object metadata | - |
| `upload_object_streaming` | Upload object | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
