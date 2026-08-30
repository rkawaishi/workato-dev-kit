# ServiceNow recipes

Provider value to use in every step: `service_now`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "service_now"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (9)

| Internal name | Title | Batch |
|---|---|---|
| `new_object` | New record | - |
| `new_object_webhook` | New record | - |
| `object_batch_created` | New record | yes |
| `object_batch_created_or_updated` | New/updated record | yes |
| `object_created_bulk` | Export new records | - |
| `object_created_or_updated_bulk` | Export new/updated records | - |
| `scheduled_query` | Scheduled record search | yes |
| `updated_object` | New/updated record | - |
| `updated_object_webhook` | New/updated record | - |


## Actions (10)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_object` | Create record | - |
| `create_object_using_template` | Create record using a template | - |
| `download_attachment` | Get attachment contents | - |
| `get_table_schema` | Get object schema | - |
| `search_objects_v2` | Search records | yes |
| `search_using_query` | Search records using query | yes |
| `update_object` | Update record | - |
| `update_object_using_template` | Update record using a template | - |
| `upload_attachment` | Upload attachment | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `closed_incident` | Closed incident | - |
| `new_incident` | New incident | - |
| `new_sys_user` | New user | - |
| `updated_incident` | New/updated incident | - |
| `updated_sys_user` | New/updated user | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `assign_user_to_incident` | Assign user to incident | - |
| `create_asset` | Create asset | - |
| `create_catalog_task` | Create catalog task | - |
| `create_change` | Create change | - |
| `create_core_company` | Create core company | - |
| `create_incident` | Create incident | - |
| `create_problem` | Create problem | - |
| `create_user` | Create user | - |
| `get_incident` | Get incident details by ID | - |
| `get_user` | Get user details by ID | - |
| `lookup_user` | Search users | - |
| `search_assets` | Search assets | - |
| `search_companies` | Search companies | - |
| `search_objects` | Search records | - |
| `search_users` | Search users | - |
| `update_asset` | Update asset | - |
| `update_company` | Update company | - |
| `update_incident` | Update incident | - |
| `update_user` | Update user | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
