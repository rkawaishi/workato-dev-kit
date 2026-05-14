# Azure Blob Storage connector

Provider: `azure_blob_storage`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New blob | `new_blob` | - |  |
| New event | `new_event_webhook` | - |  |

## Actions

| Name | Internal name | Batch | Description |
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
