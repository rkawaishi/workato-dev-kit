# Adobe Experience Manager recipes

Provider value to use in every step: `adobe_experience_manager`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "adobe_experience_manager"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_asset_or_folder` | New asset or folder | - |
| `new_or_updated_asset` | New or updated asset | - |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `copy_folder_asset` | Copy folder/asset | - |
| `create_folder` | Create folder | - |
| `delete_folder_asset` | Delete folder/asset | - |
| `download_asset` | Download asset | - |
| `move_folder_asset` | Move folder/asset | - |
| `search_assets` | Search assets | yes |
| `update_asset_metadata` | Update asset metadata | - |
| `upload_asset` | Upload asset | - |
| `upload_asset_streaming` | Upload asset by streaming | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
