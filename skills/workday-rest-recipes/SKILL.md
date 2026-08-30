# Workday REST recipes

Provider value to use in every step: `workday_rest`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "workday_rest"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_worker` | New worker | - |


## Actions (23)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `cancel_business_process_event` | Cancel business process event | - |
| `create_job_changes` | Create a job change | - |
| `get_absence_balances` | Get absence balances | - |
| `get_business_process_events` | Get business process events | - |
| `get_business_process_types` | Get business process types | - |
| `get_direct_reports` | Get direct reports | - |
| `get_eligible_absence_types` | Get eligible absence types | - |
| `get_event_in_progress_steps` | Get event in-progress steps | - |
| `get_inbox_tasks` | Get inbox task(s) | yes |
| `get_staffing_worker` | Get worker (Staffing) | - |
| `get_supervisory_organization` | Get supervisory organization by ID | - |
| `get_time_off_details` | Get time off details | - |
| `get_time_off_entry` | Get time off entry | - |
| `get_time_off_request` | Get time off request | - |
| `get_time_off_status_values` | Get time off status values | - |
| `get_valid_time_off_dates` | Get valid time off dates | - |
| `get_worker` | Get worker by ID | - |
| `get_worker_service_dates` | Get worker service dates | - |
| `list_time_off_entries` | List time off entries | - |
| `request_time_off` | Request time off | - |
| `search_workers` | Search workers | yes |
| `update_inbox_task` | Approve/reject an inbox task | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
