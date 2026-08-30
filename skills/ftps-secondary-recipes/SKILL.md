# FTP/FTPS secondary recipes

Provider value to use in every step: `ftps_secondary`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "ftps_secondary"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_csv_file` | New CSV file | yes |
| `new_file_in_dir` | New/updated file in directory | - |


## Actions (7)

| Internal name | Title | Batch |
|---|---|---|
| `get_file_content` | Download file | - |
| `list_directories_files` | List files and directories | yes |
| `remove` | Remove file | - |
| `rename` | Rename file | - |
| `stat` | Get file information | - |
| `streamable_get_file_content` | Download large file | - |
| `upload` | Upload file | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
