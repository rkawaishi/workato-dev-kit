# BIM 360 recipes

Provider value to use in every step: `bim360`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "bim360"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `new_updated_document_in_project` | New or updated document in a project folder | - |
| `new_updated_document_in_project_subfolders` | New or updated document in a project folder and subfolders | - |
| `new_updated_issue_in_project_v2` | New or updated issue (V2) in a project | - |
| `new_updated_object_in_project` | New or updated object in a project | - |


## Actions (19)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_issue_in_project_v2` | Create issue in a project (V2) | - |
| `create_object_in_project` | Create object in a project | - |
| `download_cost_document_in_project` | Download cost document in a project | - |
| `download_document` | Download document in a project | - |
| `download_drawing_export` | Download drawing export in a project | - |
| `export_project_plan` | Export drawing in a project | - |
| `get_document_in_project` | Get document in a project | - |
| `get_drawing_export_status` | Get drawing export status in a project | - |
| `get_folder_contents` | Get folder contents | yes |
| `get_folder_details` | Get folder info in a project | - |
| `get_issue_in_project_v2` | Get issue in a project (V2) | - |
| `get_object_in_project` | Get object in a project | - |
| `get_project_details` | Get project details | - |
| `search_issues_in_project_v2` | Search issues in a project (V2) | yes |
| `search_objects_in_project` | Search objects in a project | - |
| `update_issue_in_project_v2` | Update issue in a project (V2) | - |
| `update_object_in_project` | Update object in a project | - |
| `upload_document_to_project` | Upload document to a project | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_updated_issue_in_project` | New or updated issue in a project | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `create_issue_in_project` | Create issue in a project | - |
| `custom_action` | Custom action | - |
| `get_issue_in_project` | Get issue in a project | - |
| `search_issues_in_project` | Search issues in a project | yes |
| `update_issue_in_project` | Update issue in a project | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
