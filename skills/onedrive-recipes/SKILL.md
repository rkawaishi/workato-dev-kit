# OneDrive recipes

Provider value to use in every step: `onedrive`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "onedrive"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (5)

| Internal name | Title | Batch |
|---|---|---|
| `new_csv_line` | New line in CSV file | - |
| `new_event_trigger` | New event | - |
| `new_file` | New file | - |
| `new_folder` | New folder | - |
| `updated_file` | New/updated file | - |


## Actions (12)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_folder` | Create folder | - |
| `create_permission` | Add permission | - |
| `delete_file_or_folder` | Delete file or folder | - |
| `delete_permission` | Remove permission | - |
| `download_file` | Download File | - |
| `list_files_folders` | List files and folders | yes |
| `list_permission` | List permissions | yes |
| `search_files_new` | Search files | yes |
| `upload_file` | Upload file via file content | - |
| `upload_file_from_url` | Upload file from URL | - |
| `upload_file_session` | Upload large file via session | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `search_files` | Search files | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
