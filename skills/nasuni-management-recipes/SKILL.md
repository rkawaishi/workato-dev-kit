# Nasuni Management Console recipes

Provider value to use in every step: `nasuni_management`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "nasuni_management"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_notification` | New notification | - |


## Actions (25)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `auto_caching_for_file` | Set auto caching mode for file/directory | - |
| `bring_path_into_cache` | Brings a specified file/directory into volume cache | - |
| `create_directory` | Creates a directory in a volume | - |
| `create_folder_quota` | Create folder quota for a specified volume | - |
| `create_share` | Create share | - |
| `create_volume` | Create volume | - |
| `delete_folder_quota` | Deletes folder quota for a specified volume | - |
| `disable_auto_cache_mode` | Disables auto cache mode for file/directory | - |
| `disable_pinning_mode_for_folder` | Disable pinning mode for file/directory | - |
| `get_auto_cache_status` | Retrieves auto cache status for file/directory | - |
| `get_folder_quota` | Get folder quota from a specified volume | - |
| `get_health_status_for_filer` | Get health status for a filer | yes |
| `get_info_path` | Get file/directory | - |
| `get_pinning_status_for_path` | Retrieves pinning status for file/directory | - |
| `global_lock_folders` | Enable global locking for file/folders | - |
| `list_folder_quotas` | List all folder quotas | yes |
| `list_folder_quotas_volume` | List folder quotas for a specified volume | yes |
| `list_health_status_for_filer` | List health status for all filers | - |
| `list_shares` | List shares in Nasuni Management Console | yes |
| `list_volumes` | List Volumes | yes |
| `pin_data_to_cache` | Pin file/directory into cache | - |
| `request_snapshot_volume` | Request snapshot for volume | - |
| `update_folder_quota` | Update folder quota for a specified volume | - |
| `update_share` | Update share | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
