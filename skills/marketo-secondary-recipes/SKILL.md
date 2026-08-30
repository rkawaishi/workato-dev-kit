# Marketo secondary recipes

Provider value to use in every step: `marketo_secondary`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "marketo_secondary"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (8)

| Internal name | Title | Batch |
|---|---|---|
| `lead_created_bulk` | Export new leads in Marketo | - |
| `lead_created_or_updated_bulk` | Export new/updated leads in Marketo | - |
| `monitor_leads_added_list_batch` | Monitor leads added to list | yes |
| `new_lead_activity_batch` | New lead activity | yes |
| `new_lead_in_list` | New lead in list | - |
| `new_marketo_async_submission` | New Marketo Self Service Flow Step | - |
| `new_updated_lead_batch` | New/updated lead | yes |
| `updated_lead` | New/updated lead | - |


## Actions (21)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `activate_smart_campaign` | Activate smart campaign | - |
| `add_custom_activity` | Add custom activity | yes |
| `add_leads_to_list` | Add leads to lead list | yes |
| `bulk_export_objects_action` | Bulk export objects to file | - |
| `bulk_import_objects_action` | Bulk import objects from file | - |
| `change_lead_program_status` | Change lead program status | yes |
| `clone_objects_action` | Clone object | - |
| `create_objects_action` | Create object | - |
| `get_objects_action` | Get objects | - |
| `remove_leads_from_list` | Remove leads from lead list | - |
| `return_marketo_async_action_result` | Return data to Marketo Self Service Flow Step | - |
| `schedule_campaign` | Schedule campaign or smart campaign | - |
| `search_objects_action` | Search objects | yes |
| `submit_form` | Submit form | - |
| `trigger_campaign` | Trigger campaign or smart campaign for specific leads | - |
| `update_objects_action` | Update object | - |
| `upsert_custom_objects` | Upsert custom objects | yes |
| `upsert_lead` | Create/update/upsert leads | yes |
| `upsert_object` | Upsert object | - |
| `upsert_tokens` | Upsert tokens | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `bulk_custom_object_import_csv` | Bulk import custom object from file | yes |
| `bulk_export_custom_objects` | Bulk export custom objects to file | yes |
| `bulk_export_program_members` | Bulk export program members to file | yes |
| `bulk_import_program_members` | Bulk import program members from file | yes |
| `bulk_lead_import_csv` | Bulk import leads from file | yes |
| `clone_program` | Clone program | - |
| `create_custom_objects` | Create custom objects | - |
| `create_lead` | Create lead | - |
| `create_opportunity` | Create opportunity | - |
| `create_opportunity_role` | Create opportunity role | - |
| `create_program` | Create program | - |
| `fetch_lead_activities` | Get lead activities | - |
| `find_campaigns` | Search campaigns | - |
| `get_channel_by_name` | Get channel by name | - |
| `get_object_schema` | Get object schema | - |
| `get_program_by_name` | Get program by name | - |
| `query_tokens` | Get tokens by folder ID | - |
| `search_activity_bulk` | Bulk export activities to file | yes |
| `search_custom_objects` | Search custom objects | - |
| `search_lead_bulk` | Bulk export leads to file | yes |
| `search_leads` | Search leads | - |
| `search_opportunities` | Search opportunities | - |
| `search_opportunity_roles` | Search opportunity roles | - |
| `search_programs` | Search programs | - |
| `update_custom_object` | Update custom object | - |
| `update_lead` | Update lead | - |
| `update_opportunity` | Update opportunity | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
