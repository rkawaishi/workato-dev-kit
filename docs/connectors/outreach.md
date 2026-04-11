# Outreach コネクタ

Provider: `outreach`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Completed sequence task | `completed_sequence_task` | - |  |
| New or updated record | `new_or_updated_record` | - |  |
| New record | `new_record` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add a prospect to sequence | `add_prospect_to_sequence` | - |  |
| Add a template to sequence step | `add_template_to_sequence_step` | - |  |
| Create record | `create_object` | - |  |
| Get record by ID | `get_object` | - |  |
| Get steps in a sequence | `get_steps_in_sequence` | Yes |  |
| Search records | `search_object` | Yes |  |
| Update record | `update_object` | - |  |
