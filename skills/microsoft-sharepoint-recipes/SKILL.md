# Microsoft Sharepoint recipes

Provider value to use in every step: `microsoft_sharepoint`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "microsoft_sharepoint"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (6)

| Internal name | Title | Batch |
|---|---|---|
| `deleted_file_folder` | Deleted File or Folder | - |
| `new_row_in_sharepoint_list` | New row in Sharepoint list | - |
| `new_updated_file_in_folder_hierarchy` | New/updated file in folder hierarchy | - |
| `new_updated_file_in_folder_hierarchy_v2` | New/updated file in folder hierarchy (large site) | - |
| `new_updated_file_in_sharepoint_library` | New or updated file | - |
| `new_updated_row_in_sharepoint_list` | New/updated row in Sharepoint list | - |


## Actions (23)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_row_in_sharepoint_list` | Add row in Sharepoint list | - |
| `copy_file` | Copy file | - |
| `create_folder` | Create Folder | - |
| `create_row_in_sharepoint_list_batch` | Create rows | yes |
| `delete_file_from_library` | Delete file or folder from library | - |
| `delete_row_in_sharepoint_list` | Delete row | - |
| `download_attachment` | Download attachment | - |
| `download_file_from_library` | Download file from library | - |
| `get_file_folder` | Get file and folder details | - |
| `get_permission` | Get file or folder permissions | yes |
| `list_files_folders` | List files and folders within a folder | yes |
| `move_file` | Move file | - |
| `rename_file_folder` | Rename file or folder | - |
| `search_file_by_name` | Search files | yes |
| `search_list_items_v2` | Search list items | yes |
| `search_users` | Search users | yes |
| `update_file_in_library` | Update file using file contents | - |
| `update_file_metadata` | Update file metadata | - |
| `update_row_in_sharepoint_list` | Update row | - |
| `update_row_in_sharepoint_list_batch` | Update rows | yes |
| `upload_attachment` | Upload attachment | - |
| `upload_file_in_library` | Upload file in library | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `search_list_items` | Search list items | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
