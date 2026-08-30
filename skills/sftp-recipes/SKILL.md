# SFTP recipes

Provider value to use in every step: `sftp`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "sftp"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_csv_file` | New/updated CSV file in directory | yes |
| `new_file_in_dir` | New/updated file in directory | - |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `dir` | List folder | yes |
| `mkdir` | Create folder | - |
| `remove` | Delete file | - |
| `remove_folder` | Delete folder | - |
| `rename` | Rename/move file | - |
| `search_files_folders` | Search files/folders | yes |
| `set_permissions` | Change permission of a file or a folder | - |
| `stat` | Get file information | - |
| `streamable_download` | Download file | - |
| `upload` | Upload file | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `copy` | Copy file | - |
| `download` | Download file | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
