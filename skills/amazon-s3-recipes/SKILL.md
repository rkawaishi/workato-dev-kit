# Amazon S3 recipes

Provider value to use in every step: `amazon_s3`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "amazon_s3"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `new_CSV_file` | New CSV file | - |
| `new_file` | New file | - |
| `new_file_slice` | New file slice | - |
| `new_updated_file` | New/updated file or folder | - |


## Actions (9)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `copy_object` | Copy file | - |
| `create_bucket` | Create bucket | - |
| `delete_bucket` | Delete bucket | - |
| `delete_file` | Delete file/folder | - |
| `generate_presigned_url` | Generate presigned URL | - |
| `get_file` | Download file contents | - |
| `list_bucket` | List files in bucket | yes |
| `upload_file` | Upload file | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `upload_file_streaming` | Upload file (streaming) | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
