# Marketo secondary コネクタ

Provider: `marketo_secondary`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Export new leads in Marketo | `lead_created_bulk` | - |  |
| Export new/updated leads in Marketo | `lead_created_or_updated_bulk` | - |  |
| Monitor leads added to list | `monitor_leads_added_list_batch` | Yes |  |
| New lead activity | `new_lead_activity_batch` | Yes |  |
| New lead in list | `new_lead_in_list` | - |  |
| New Marketo Self Service Flow Step | `new_marketo_async_submission` | - |  |
| New/updated lead | `new_updated_lead_batch` | Yes |  |
| New/updated lead | `updated_lead` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Activate smart campaign | `activate_smart_campaign` | - |  |
| Add custom activity | `add_custom_activity` | Yes |  |
| Add leads to lead list | `add_leads_to_list` | Yes |  |
| Bulk import custom object from file | `bulk_custom_object_import_csv` | Yes |  [deprecated] |
| Bulk export custom objects to file | `bulk_export_custom_objects` | Yes |  [deprecated] |
| Bulk export objects to file | `bulk_export_objects_action` | - |  |
| Bulk export program members to file | `bulk_export_program_members` | Yes |  [deprecated] |
| Bulk import objects from file | `bulk_import_objects_action` | - |  |
| Bulk import program members from file | `bulk_import_program_members` | Yes |  [deprecated] |
| Bulk import leads from file | `bulk_lead_import_csv` | Yes |  [deprecated] |
| Change lead program status | `change_lead_program_status` | Yes |  |
| Clone object | `clone_objects_action` | - |  |
| Clone program | `clone_program` | - |  [deprecated] |
| Create custom objects | `create_custom_objects` | - |  [deprecated] |
| Create lead | `create_lead` | - |  [deprecated] |
| Create object | `create_objects_action` | - |  |
| Create opportunity | `create_opportunity` | - |  [deprecated] |
| Create opportunity role | `create_opportunity_role` | - |  [deprecated] |
| Create program | `create_program` | - |  [deprecated] |
| Get lead activities | `fetch_lead_activities` | - |  [deprecated] |
| Search campaigns | `find_campaigns` | - |  [deprecated] |
| Get channel by name | `get_channel_by_name` | - |  [deprecated] |
| Get object schema | `get_object_schema` | - |  [deprecated] |
| Get objects | `get_objects_action` | - |  |
| Get program by name | `get_program_by_name` | - |  [deprecated] |
| Get tokens by folder ID | `query_tokens` | - |  [deprecated] |
| Remove leads from lead list | `remove_leads_from_list` | - |  |
| Return data to Marketo Self Service Flow Step | `return_marketo_async_action_result` | - |  |
| Schedule campaign or smart campaign | `schedule_campaign` | - |  |
| Bulk export activities to file | `search_activity_bulk` | Yes |  [deprecated] |
| Search custom objects | `search_custom_objects` | - |  [deprecated] |
| Bulk export leads to file | `search_lead_bulk` | Yes |  [deprecated] |
| Search leads | `search_leads` | - |  [deprecated] |
| Search objects | `search_objects_action` | Yes |  |
| Search opportunities | `search_opportunities` | - |  [deprecated] |
| Search opportunity roles | `search_opportunity_roles` | - |  [deprecated] |
| Search programs | `search_programs` | - |  [deprecated] |
| Submit form | `submit_form` | - |  |
| Trigger campaign or smart campaign for specific leads | `trigger_campaign` | - |  |
| Update custom object | `update_custom_object` | - |  [deprecated] |
| Update lead | `update_lead` | - |  [deprecated] |
| Update object | `update_objects_action` | - |  |
| Update opportunity | `update_opportunity` | - |  [deprecated] |
| Upsert custom objects | `upsert_custom_objects` | Yes |  |
| Create/update/upsert leads | `upsert_lead` | Yes |  |
| Upsert object | `upsert_object` | - |  |
| Upsert tokens | `upsert_tokens` | - |  |
