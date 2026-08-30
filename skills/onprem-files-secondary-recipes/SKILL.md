# On-prem files secondary recipes

Provider value to use in every step: `onprem_files_secondary`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "onprem_files_secondary"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `csv_file_batch` | New CSV file in folder | yes |
| `new_csv_file_batch` | New lines in CSV file | yes |
| `new_csv_file_line` | New line in CSV file | - |
| `new_file` | New file in folder | - |


## Actions (11)

| Internal name | Title | Batch |
|---|---|---|
| `add_csv_line` | Append line to CSV file | - |
| `create_folder` | Create folder | - |
| `delete_file` | Delete file | - |
| `delete_folder` | Delete folder | - |
| `download_file` | Download file | - |
| `generate_file_url` | Generate on-prem file URL | - |
| `list_files` | List files in folder | yes |
| `move_file` | Move file | - |
| `rename_file` | Rename file | - |
| `upload_file` | Upload file (Legacy) | - |
| `upload_file_multistep` | Upload file | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_or_changed_file` | New/updated files and folders | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `append_file_content` | Append content to file | - |
| `download_file_contents` | Download file contents | - |
| `read_csv_file_lines` | Read lines from CSV file | - |
| `update_csv_line` | Update line in CSV file | - |
| `upload_file_content` | Send file in directory | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
