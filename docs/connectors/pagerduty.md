# Pagerduty コネクタ

Provider: `pagerduty`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New incident | `new_incident` | - |  |
| New notification | `new_notification` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add note to incident | `add_note_to_incident` | - |  |
| Get incident by ID | `get_incident_by_ID` | - |  |
| List log entries | `list_log_entries` | Yes |  |
| Search incident | `search_incident` | Yes |  |
| Send an event | `send_an_event` | - |  |
| Update incident | `update_incident` | - |  |
