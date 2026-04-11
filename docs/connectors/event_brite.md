# Eventbrite コネクタ

Provider: `event_brite`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New contact created | `new_contact` | - |  |
| New event created | `new_user_event` | - |  |
| New attendee registered for event | `new_user_event_attendee` | - |  |
| New order for event | `new_user_event_order` | - |  |
| New/updated attendee registered for event | `updated_user_event_attendee` | - |  |
| New/updated attendee registered for event | `updated_user_event_attendee_webhook` | - |  |
| New/updated order for event | `updated_user_event_order` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create/update contact | `create_contact` | - |  |
| Create contact list | `create_contact_list` | - |  |
| Get event attendees | `get_attendees` | Yes |  |
| Search events | `search_events` | Yes |  |
