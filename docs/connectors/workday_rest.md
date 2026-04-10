# Workday REST コネクタ

Provider: `workday_rest`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New worker | `new_worker` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Cancel business process event | `cancel_business_process_event` | - |  |
| Create a job change | `create_job_changes` | - |  |
| Get absence balances | `get_absence_balances` | - |  |
| Get business process events | `get_business_process_events` | - |  |
| Get business process types | `get_business_process_types` | - |  |
| Get direct reports | `get_direct_reports` | - |  |
| Get eligible absence types | `get_eligible_absence_types` | - |  |
| Get event in-progress steps | `get_event_in_progress_steps` | - |  |
| Get inbox task(s) | `get_inbox_tasks` | Yes |  |
| Get worker (Staffing) | `get_staffing_worker` | - |  |
| Get supervisory organization by ID | `get_supervisory_organization` | - |  |
| Get time off details | `get_time_off_details` | - |  |
| Get time off entry | `get_time_off_entry` | - |  |
| Get time off request | `get_time_off_request` | - |  |
| Get time off status values | `get_time_off_status_values` | - |  |
| Get valid time off dates | `get_valid_time_off_dates` | - |  |
| Get worker by ID | `get_worker` | - |  |
| Get worker service dates | `get_worker_service_dates` | - |  |
| List time off entries | `list_time_off_entries` | - |  |
| Request time off | `request_time_off` | - |  |
| Search workers | `search_workers` | Yes |  |
| Approve/reject an inbox task | `update_inbox_task` | - |  |
