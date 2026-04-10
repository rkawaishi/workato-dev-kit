# Workday コネクタ

Provider: `workday`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New/updated business object | `new_updated_object` | - |  |
| New/updated business object | `new_updated_object_batch` | Yes |  |
| Scheduled report fetch | `scheduled_report_batch` | Yes |  |
| Scheduled report fetch using WQL | `scheduled_wql_report_batch` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Get business object details | `Get_business_object_details` | Yes |  |
| Search business object | `Search_business_object` | Yes |  |
| Update business object | `Update_business_object` | - |  |
| Custom action | `__adhoc_http_action` | - |  |
| Call operation | `call_operation` | - |  |
| Get custom objects | `get_custom_object` | - |  |
| Get report | `get_report` | - |  |
| Get report using WQL | `get_wql_report` | Yes |  |
| List custom object definitions | `list_custom_objects` | Yes |  |
| Create/update custom object | `post_custom_object` | - |  |
