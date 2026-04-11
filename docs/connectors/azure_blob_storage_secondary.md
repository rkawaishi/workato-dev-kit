# Azure Blob Storage secondary コネクタ

Provider: `azure_blob_storage_secondary`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New blob | `new_blob` | - |  |
| New event | `new_event_webhook` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create container | `create_container` | - |  |
| Download blob contents | `download_blob` | - |  |
| Generate pre-signed URL | `generate_presigned_url` | - |  |
| Get blob properties | `get_blob_properties` | - |  |
| Get container properties | `get_container_properties` | - |  |
| Search blobs | `search_blob` | Yes |  |
| Search containers | `search_container` | Yes |  |
| Update blob metadata | `update_blob_metadata` | - |  |
| Upload blob | `upload_blob` | - |  |
