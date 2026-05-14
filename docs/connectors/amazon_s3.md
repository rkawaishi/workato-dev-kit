# Amazon S3 connector

Provider: `amazon_s3`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New CSV file | `new_CSV_file` | - |  |
| New file | `new_file` | - |  |
| New file slice | `new_file_slice` | - |  |
| New/updated file or folder | `new_updated_file` | - |  |

## Actions

| Name | Internal name | Batch | Description |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Copy file | `copy_object` | - |  |
| Create bucket | `create_bucket` | - |  |
| Delete bucket | `delete_bucket` | - |  |
| Delete file/folder | `delete_file` | - |  |
| Generate presigned URL | `generate_presigned_url` | - |  |
| Download file contents | `get_file` | - |  |
| List files in bucket | `list_bucket` | Yes |  |
| Upload file | `upload_file` | - |  |
| Upload file (streaming) | `upload_file_streaming` | - |  [deprecated] |
