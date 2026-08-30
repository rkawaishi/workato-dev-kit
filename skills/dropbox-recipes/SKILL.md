# Dropbox recipes

Provider value to use in every step: `dropbox`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "dropbox"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (6)

| Internal name | Title | Batch |
|---|---|---|
| `file_revision` | New file revision | - |
| `new_batch_csv_file_lines` | New lines in CSV file | yes |
| `new_csv_file_line` | New line in CSV file | - |
| `new_or_changed_file` | New/updated file in directory | - |
| `new_or_updated_csv_file` | New/updated CSV file in directory | - |
| `updated_csv_file_line` | New/updated line in CSV file | - |


## Actions (15)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `copy_file` | Copy file or folder | - |
| `create_folder` | Create folder | - |
| `delete_file` | Delete file or folder | - |
| `fetch_deleted_files_and_folders` | Fetch deleted files and folders | - |
| `file_download` | Download file | - |
| `get_metadata` | Get metadata of a file or folder | - |
| `move_file` | Move/rename file or folder | - |
| `read_csv_file_lines` | Read CSV file lines | yes |
| `search_files` | Search files | yes |
| `search_folder` | Search folders | yes |
| `update_csv_file` | Update CSV file in dropbox | - |
| `upload_file_content_stream` | Upload file using file contents | - |
| `upload_file_from_url` | Upload file from URL | - |
| `upload_multiline_file` | Upload multiline file | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `upload_file_content` | Upload file using file contents | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
