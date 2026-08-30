# Workato FileStorage recipes

Provider value to use in every step: `workato_files`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workato_files"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `new_csv_file` | New CSV file | yes |
| `new_file` | New File | - |
| `new_lines_in_csv_file` | New lines in CSV file | yes |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `append_to_file` | Append to file | - |
| `create_shareable_link` | Generate shareable file link | - |
| `delete_directory` | Delete directory | - |
| `delete_file` | Delete file | - |
| `ensure_dir_exists` | Create directory | - |
| `get_csv_file_contents` | Get lines from CSV file | yes |
| `get_file_contents` | Get file contents | - |
| `move_file` | Rename/move file | - |
| `search_files` | Search files | yes |
| `store_file` | Create file | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
