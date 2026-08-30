# Bynder recipes

Provider value to use in every step: `bynder`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "bynder"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_asset` | New asset | - |
| `new_or_updated_asset` | New/updated asset | - |


## Actions (13)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_assets_to_collection` | Add assets to collection | - |
| `add_tag_to_assets` | Add tag to assets | - |
| `create_asset_usage` | Create asset usage | - |
| `delete_assets_from_collections` | Delete assets from collection | - |
| `download_asset` | Download asset | - |
| `get_records` | Get record details by ID | - |
| `list_brands` | List brands | yes |
| `retrieve_assets_in_collection` | Retrieve assets in collection | yes |
| `search_records` | Search records | yes |
| `share_collection` | Share collection | - |
| `update_record` | Update record | - |
| `upload_asset` | Upload asset | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
