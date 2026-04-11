# Outlook コネクタ

Provider: `outlook`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Deleted event | `delete_deleted_event` | - |  |
| New contact | `new_contact` | - |  |
| New email | `new_email` | - |  |
| New event | `new_event` | - |  [deprecated] |
| New event | `new_event_v2` | - |  |
| New/updated contact | `new_updated_contact` | - |  |
| New/updated email | `updated_email` | - |  |
| New/updated event | `updated_event` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create calendar | `create_calendar` | - |  |
| Create contact | `create_contact` | - |  |
| Create calendar event | `create_event` | - |  |
| Delete calendar event | `delete_calendar_event` | - |  |
| Delete contact | `delete_contact` | - |  |
| Download email attachments | `get_attachments` | - |  |
| Get calendar by ID | `get_calendar` | - |  |
| Get contact | `get_contact` | - |  |
| Get calendar event by ID | `get_event` | - |  |
| List calendars | `list_calendars_outlook` | - |  |
| List contacts | `list_contact` | Yes |  |
| List all instances of an event | `list_event_instances` | Yes |  |
| Search calendar | `search_calendar` | Yes |  |
| Search contacts | `search_contact` | Yes |  |
| Search calendar events | `search_events` | Yes |  |
| Send email | `send_mail` | - |  |
| Update contact | `update_contact` | - |  |
| Update calendar event | `update_event` | - |  |
