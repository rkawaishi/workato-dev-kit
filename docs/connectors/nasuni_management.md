# Nasuni Management Console コネクタ

Provider: `nasuni_management`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New notification | `new_notification` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Set auto caching mode for file/directory | `auto_caching_for_file` | - |  |
| Brings a specified file/directory into volume cache | `bring_path_into_cache` | - |  |
| Creates a directory in a volume | `create_directory` | - |  |
| Create folder quota for a specified volume | `create_folder_quota` | - |  |
| Create share | `create_share` | - |  |
| Create volume | `create_volume` | - |  |
| Deletes folder quota for a specified volume | `delete_folder_quota` | - |  |
| Disables auto cache mode for file/directory | `disable_auto_cache_mode` | - |  |
| Disable pinning mode for file/directory | `disable_pinning_mode_for_folder` | - |  |
| Retrieves auto cache status for file/directory | `get_auto_cache_status` | - |  |
| Get folder quota from a specified volume | `get_folder_quota` | - |  |
| Get health status for a filer | `get_health_status_for_filer` | Yes |  |
| Get file/directory | `get_info_path` | - |  |
| Retrieves pinning status for file/directory | `get_pinning_status_for_path` | - |  |
| Enable global locking for file/folders | `global_lock_folders` | - |  |
| List all folder quotas | `list_folder_quotas` | Yes |  |
| List folder quotas for a specified volume | `list_folder_quotas_volume` | Yes |  |
| List health status for all filers | `list_health_status_for_filer` | - |  |
| List shares in Nasuni Management Console | `list_shares` | Yes |  |
| List Volumes | `list_volumes` | Yes |  |
| Pin file/directory into cache | `pin_data_to_cache` | - |  |
| Request snapshot for volume | `request_snapshot_volume` | - |  |
| Update folder quota for a specified volume | `update_folder_quota` | - |  |
| Update share | `update_share` | - |  |
