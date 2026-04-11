# Greenhouse コネクタ

Provider: `greenhouse`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New event | `new_event` | - |  |
| New object | `new_object` | - |  [deprecated] |
| New object (v3) | `new_object_v3` | - |  |
| New/updated object | `new_or_updated_objects_batch` | Yes |  [deprecated] |
| New/updated object (v3) | `new_or_updated_objects_batch_v3` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Advance application | `advance_application` | - |  [deprecated] |
| Create attachment (v3) | `create_attachment_v3` | - |  |
| Create object | `create_object` | - |  [deprecated] |
| Create object (v3) | `create_object_v3_post` | - |  |
| Get object by ID | `get_object` | - |  [deprecated] |
| Mark candidate as hired | `mark_candidate_hire` | - |  [deprecated] |
| Mark candidate as hired (v3) | `mark_candidate_hire_v3` | - |  |
| Move application (v3) | `move_application_v3` | - |  |
| Reject application | `reject_application` | - |  [deprecated] |
| Reject application (v3) | `reject_application_v3` | - |  |
| Search object | `search_object` | Yes |  [deprecated] |
| Search objects (v3) | `search_object_v3` | Yes |  |
| Update object | `update_object` | - |  [deprecated] |
| Update object (v3) | `update_object_v3_patch` | - |  |
| Upload attachment | `upload_attachment` | - |  [deprecated] |
