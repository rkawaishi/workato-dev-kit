# Google Calendar recipes

Provider value to use in every step: `google_calendar`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "google_calendar"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `event_end` | Event end | - |
| `event_start` | Event start | - |
| `new_event` | New event | - |
| `updated_event` | New/updated event | - |


## Actions (14)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_attendee_to_an_event` | Add attendees to an event | yes |
| `create_allday_event` | Create all day event | - |
| `create_calendar` | Create calendar | - |
| `create_event` | Create event | - |
| `create_task` | Create task | - |
| `delete_attendees_from_an_event` | Delete attendees from an event | yes |
| `delete_event` | Delete event | - |
| `get_calendar_by_id` | Get calendar by ID | - |
| `get_event_by_id` | Get event by ID | - |
| `list_calendars_public` | List calendars | - |
| `search_events` | Search events | yes |
| `update_event` | Update event | - |
| `update_task` | Update task | - |


## Field details

Input/output field definitions observed from the Workato UI. The Workato API does not expose these, so treat them as the authoritative source for required fields and types.

### event_end (Event end)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select a calendar to monitor for event end. |
| Search term | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Calendar ID | text | — |
| Kind | text | — |
| Etag | text | — |
| Color ID | text | — |
| Event import ID | text | — |
| ID | text | — |
| Status | text | — |
| URL | text | — |
| Created | date-time | — |
| Updated | date-time | — |
| Summary | text | — |
| Description | text | — |
| Location | text | — |
| Start | date-time | — |
| End | date-time | — |
| Recurrence | text-array | — |
| Recurring event ID | text | — |
| Original start time | object | — |
| Date time | date-time | — |
| Time zone | text | — |
| Visibility | text | — |
| Reminders | object | — |
| Use default | boolean | — |
| Overrides | array | — |
| Show me as | text | — |
| Hangout link | text | — |
| Sequence | integer | — |
| Guests can modify | boolean | — |
| Guests can see other guests | boolean | — |
| Attachments | array | — |
| File URL | text | — |
| Title | text | — |
| Mime type | text | — |
| Icon link | text | — |
| File ID | text | — |
| List size | integer | — |
| List index | integer | — |
| Attendees | array | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Response status | text | — |
| Comment | text | — |
| List size | integer | — |
| List index | integer | — |
| Creator | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Organizer | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Conference data | object | — |
| Create request | object | — |
| Entry points | array | — |
| Conference solution | object | — |
| Conference ID | text | — |
| Signature | text | — |
| Notes | text | — |
| Focus time properties | object | — |
| Auto decline mode | text | — |
| Decline message | text | — |
| Chat status | text | — |
| Out of office properties | object | — |
| Auto decline mode | text | — |
| Decline message | text | — |
| Working location properties | object | — |
| Type | text | — |
| Home office | text | — |
| Custom location | object | — |
| Office location | object | — |
| Event type | text | — |

### event_start (Event start)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select a calendar to monitor for event start. |
| Time before unit |  | Yes | Yes | Select a time unit for Time before event start. |
| Time before event start | integer | Yes | Yes | Enter the time before the event start you want the trigger to pick up the event. The minimum allowed duration is 5 minutes. |
| Search term | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Calendar ID | text | — |
| Kind | text | — |
| Etag | text | — |
| Color ID | text | — |
| Event import ID | text | — |
| ID | text | — |
| Status | text | — |
| URL | text | — |
| Created | date-time | — |
| Updated | date-time | — |
| Summary | text | — |
| Description | text | — |
| Location | text | — |
| Start | date-time | — |
| End | date-time | — |
| Recurrence | text-array | — |
| Recurring event ID | text | — |
| Original start time | object | — |
| Date time | date-time | — |
| Time zone | text | — |
| Visibility | text | — |
| Reminders | object | — |
| Use default | boolean | — |
| Overrides | array | — |
| Show me as | text | — |
| Hangout link | text | — |
| Sequence | integer | — |
| Guests can modify | boolean | — |
| Guests can see other guests | boolean | — |
| Attachments | array | — |
| File URL | text | — |
| Title | text | — |
| Mime type | text | — |
| Icon link | text | — |
| File ID | text | — |
| List size | integer | — |
| List index | integer | — |
| Attendees | array | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Response status | text | — |
| Comment | text | — |
| List size | integer | — |
| List index | integer | — |
| Creator | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Organizer | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Conference data | object | — |
| Create request | object | — |
| Entry points | array | — |
| Conference solution | object | — |
| Conference ID | text | — |
| Signature | text | — |
| Notes | text | — |
| Focus time properties | object | — |
| Auto decline mode | text | — |
| Decline message | text | — |
| Chat status | text | — |
| Out of office properties | object | — |
| Auto decline mode | text | — |
| Decline message | text | — |
| Working location properties | object | — |
| Type | text | — |
| Home office | text | — |
| Custom location | object | — |
| Office location | object | — |
| Event type | text | — |

### new_event (New event)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select a calendar to monitor for events |
| Include deleted events? | text | - | Yes | When set to true, job will be triggered for deleted events also. Defaults to false |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Calendar ID | text | — |
| Kind | text | — |
| Etag | text | — |
| Color ID | text | — |
| Event import ID | text | — |
| ID | text | — |
| Status | text | — |
| URL | text | — |
| Created | date-time | — |
| Updated | date-time | — |
| Summary | text | — |
| Description | text | — |
| Location | text | — |
| Start | date-time | — |
| End | date-time | — |
| Recurrence | text-array | — |
| Recurring event ID | text | — |
| Original start time | object | — |
| Date time | date-time | — |
| Time zone | text | — |
| Visibility | text | — |
| Reminders | object | — |
| Use default | boolean | — |
| Overrides | array | — |
| Show me as | text | — |
| Hangout link | text | — |
| Sequence | integer | — |
| Guests can modify | boolean | — |
| Guests can see other guests | boolean | — |
| Attachments | array | — |
| File URL | text | — |
| Title | text | — |
| Mime type | text | — |
| Icon link | text | — |
| File ID | text | — |
| List size | integer | — |
| List index | integer | — |
| Attendees | array | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Response status | text | — |
| Comment | text | — |
| List size | integer | — |
| List index | integer | — |
| Creator | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Organizer | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |

### updated_event (New/updated event)

Kind: Trigger
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select a calendar to monitor for events |
| Include deleted events? | text | - | Yes | When set to true, job will be triggered for deleted events also. Defaults to false |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Calendar ID | text | — |
| Kind | text | — |
| Etag | text | — |
| Color ID | text | — |
| Event import ID | text | — |
| ID | text | — |
| Status | text | — |
| URL | text | — |
| Created | date-time | — |
| Updated | date-time | — |
| Summary | text | — |
| Description | text | — |
| Location | text | — |
| Start | date-time | — |
| End | date-time | — |
| Recurrence | text-array | — |
| Recurring event ID | text | — |
| Original start time | object | — |
| Date time | date-time | — |
| Time zone | text | — |
| Visibility | text | — |
| Reminders | object | — |
| Use default | boolean | — |
| Overrides | array | — |
| Show me as | text | — |
| Hangout link | text | — |
| Sequence | integer | — |
| Guests can modify | boolean | — |
| Guests can see other guests | boolean | — |
| Attachments | array | — |
| File URL | text | — |
| Title | text | — |
| Mime type | text | — |
| Icon link | text | — |
| File ID | text | — |
| List size | integer | — |
| List index | integer | — |
| Attendees | array | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Response status | text | — |
| Comment | text | — |
| List size | integer | — |
| List index | integer | — |
| Creator | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Organizer | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |

### add_attendee_to_an_event (Add attendees to an event)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select calendar that event belongs to |
| Event ID | text | Yes | Yes | Obtain event ID from the Search events action. You can also obtain the event ID from your event URL. |
| Attendees | array | Yes | Yes | — |
| Send notifications? | text | - | Yes | If true, will notify all attendees about changed event |
| Comment | text | - | No | — |
| Optional | text | - | No | — |
| Response status | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Kind | text | — |
| Etag | text | — |
| Color ID | text | — |
| Event import ID | text | — |
| ID | text | — |
| Status | text | — |
| URL | text | — |
| Created | date-time | — |
| Updated | date-time | — |
| Summary | text | — |
| Description | text | — |
| Location | text | — |
| Start | date-time | — |
| End | date-time | — |
| Recurrence | text-array | — |
| Recurring event ID | text | — |
| Original start time | object | — |
| Date time | date-time | — |
| Time zone | text | — |
| Visibility | text | — |
| Reminders | object | — |
| Use default | boolean | — |
| Overrides | array | — |
| Show me as | text | — |
| Hangout link | text | — |
| Sequence | integer | — |
| Guests can modify | boolean | — |
| Guests can see other guests | boolean | — |
| Creator | object | — |
| Email | text | — |
| Self | boolean | — |
| Organizer | object | — |
| Email | text | — |
| Self | boolean | — |
| Attendees | array | — |
| Email | text | — |
| Name | text | — |
| Response status | text | — |
| Comment | text | — |
| Optional | boolean | — |
| Organizer | boolean | — |
| Self | boolean | — |
| List size | integer | — |
| List index | integer | — |
| Attachments | array | — |
| File URL | text | — |
| Title | text | — |
| Mime type | text | — |
| Icon link | text | — |
| File ID | text | — |
| List size | integer | — |
| List index | integer | — |

### create_allday_event (Create all day event)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select the calendar to create event in |
| Start date | date | Yes | Yes | Enter event start date |
| End date | date | - | Yes | Provide event end date for all day event |
| Displayed time zone |  | Yes | Yes | Does not change time input, only displays the date time in the selected time zone. |
| Name | text | - | Yes | Event name or summary |
| Send notifications? | text | - | Yes | This field is deprecated. This field will be overridden by send updates field. If true, sends notifications about created or updated events. |
| Event description | text | - | No | — |
| Location | text | - | No | — |
| Attendee emails | text | - | No | — |
| Send updates | text | - | No | — |
| Guests can modify? | text | - | No | — |
| Display guests list? | text | - | No | — |
| Status | text | - | No | — |
| Visibility | text | - | No | — |
| Show me as | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Kind | text | — |
| Etag | text | — |
| Color ID | text | — |
| Event import ID | text | — |
| ID | text | — |
| Status | text | — |
| URL | text | — |
| Created | date-time | — |
| Updated | date-time | — |
| Summary | text | — |
| Description | text | — |
| Location | text | — |
| Start | date-time | — |
| End | date-time | — |
| Recurrence | text-array | — |
| Recurring event ID | text | — |
| Original start time | object | — |
| Date time | date-time | — |
| Time zone | text | — |
| Visibility | text | — |
| Reminders | object | — |
| Use default | boolean | — |
| Overrides | array | — |
| Show me as | text | — |
| Hangout link | text | — |
| Sequence | integer | — |
| Guests can modify | boolean | — |
| Guests can see other guests | boolean | — |
| Attendees | array | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Response status | text | — |
| Comment | text | — |
| List size | integer | — |
| List index | integer | — |
| Creator | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Organizer | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |

### create_calendar (Create calendar)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Calendar name | text | Yes | Yes | — |
| Description | text | - | No | — |
| Time zone | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Kind | text | — |
| Etag | text | — |
| ID | text | — |
| Summary | text | — |
| Description | text | — |
| Location | text | — |
| Time zone | text | — |
| Access role | text | — |
| Conference properties | object | — |
| Allowed conference solution types | text-array | — |

### create_event (Create event)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select the calendar to create event in |
| Start date time | date-time | Yes | Yes | Event start date and time |
| End date time | date-time | Yes | Yes | Event end date and time |
| Name | text | - | Yes | Event name or summary |
| Send notifications? | text | - | Yes | This field is deprecated. This field will be overridden by send updates field. If true, sends notifications about created or updated events. |
| Displayed time zone | text | - | No | — |
| Event description | text | - | No | — |
| Location | text | - | No | — |
| Attendee emails | text | - | No | — |
| Send updates | text | - | No | — |
| Guests can modify? | text | - | No | — |
| Display guests list? | text | - | No | — |
| Status | text | - | No | — |
| Visibility | text | - | No | — |
| Show me as | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Kind | text | — |
| Etag | text | — |
| Color ID | text | — |
| Event import ID | text | — |
| ID | text | — |
| Status | text | — |
| URL | text | — |
| Created | date-time | — |
| Updated | date-time | — |
| Summary | text | — |
| Description | text | — |
| Location | text | — |
| Start | date-time | — |
| End | date-time | — |
| Recurrence | text-array | — |
| Recurring event ID | text | — |
| Original start time | object | — |
| Date time | date-time | — |
| Time zone | text | — |
| Visibility | text | — |
| Reminders | object | — |
| Use default | boolean | — |
| Overrides | array | — |
| Show me as | text | — |
| Hangout link | text | — |
| Sequence | integer | — |
| Guests can modify | boolean | — |
| Guests can see other guests | boolean | — |
| Attendees | array | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Response status | text | — |
| Comment | text | — |
| List size | integer | — |
| List index | integer | — |
| Creator | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Organizer | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |

### create_task (Create task)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Tasklist |  | Yes | Yes | — |
| Task name | text | Yes | Yes | — |
| Notes | text | - | No | — |
| Status | text | - | No | — |
| Due date | date-time | - | No | — |
| Completed date | date-time | - | No | — |
| Hidden | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| ID | text | — |
| Etag | text | — |
| Parent | text | — |
| Title | text | — |
| Description | text | — |
| Status | text | — |
| Position | text | — |
| Self link | text | — |
| Updated | date-time | — |
| Due date | date-time | — |
| Completed date | date-time | — |
| Hidden | boolean | — |
| Deleted | boolean | — |
| Links | array | — |
| Type | text | — |
| Description | text | — |
| Link | text | — |
| List size | integer | — |
| List index | integer | — |

### delete_attendees_from_an_event (Delete attendees from an event)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select calendar that event belongs to |
| Event ID | text | Yes | Yes | Obtain event ID from the Search events action. You can also obtain the event ID from your event URL. |
| Attendees | array | Yes | Yes | List of attendees to delete |
| Send notifications? | text | - | Yes | If true, will notify all attendees about changed event |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Kind | text | — |
| Etag | text | — |
| Color ID | text | — |
| Event import ID | text | — |
| ID | text | — |
| Status | text | — |
| URL | text | — |
| Created | date-time | — |
| Updated | date-time | — |
| Summary | text | — |
| Description | text | — |
| Location | text | — |
| Start | date-time | — |
| End | date-time | — |
| Recurrence | text-array | — |
| Recurring event ID | text | — |
| Original start time | object | — |
| Date time | date-time | — |
| Time zone | text | — |
| Visibility | text | — |
| Reminders | object | — |
| Use default | boolean | — |
| Overrides | array | — |
| Show me as | text | — |
| Hangout link | text | — |
| Sequence | integer | — |
| Guests can modify | boolean | — |
| Guests can see other guests | boolean | — |
| Creator | object | — |
| Email | text | — |
| Self | boolean | — |
| Display name | text | — |
| Organizer | object | — |
| Email | text | — |
| Self | boolean | — |
| Display name | text | — |
| Attendees | array | — |
| Email | text | — |
| Name | text | — |
| Response status | text | — |
| Comment | text | — |
| Optional | boolean | — |
| Organizer | boolean | — |
| Self | boolean | — |
| Additional guests | integer | — |
| List size | integer | — |
| List index | integer | — |
| Attachments | array | — |
| File URL | text | — |
| Title | text | — |
| Mime type | text | — |
| Icon link | text | — |
| File ID | text | — |
| List size | integer | — |
| List index | integer | — |

### delete_event (Delete event)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

> ⚠ Partial learning: no output schema (fire-and-forget action)

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select calendar that event belongs to |
| Event ID | text | Yes | Yes | Obtain event ID from the Search events action. You can also obtain the event ID from your event URL. |
| Send notification? | text | - | Yes | If true, will notify attendees about event being deleted |

### get_calendar_by_id (Get calendar by ID)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Calendar ID | text | Yes | Yes | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Kind | text | — |
| Etag | text | — |
| ID | text | — |
| Summary | text | — |
| Description | text | — |
| Location | text | — |
| Time zone | text | — |
| Access role | text | — |
| Conference properties | object | — |
| Allowed conference solution types | text-array | — |

### get_event_by_id (Get event by ID)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Calendar ID | text | Yes | Yes | ID of calendar that event belongs to. Click calendar settings in the drop down menu next to the specific calendar. Get calendar ID from calendar address field. |
| Event ID | text | Yes | Yes | Obtain event ID from the Search events action. You can also obtain the event ID from your event URL. |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Kind | text | — |
| Etag | text | — |
| Color ID | text | — |
| Event import ID | text | — |
| ID | text | — |
| Status | text | — |
| URL | text | — |
| Created | date-time | — |
| Updated | date-time | — |
| Summary | text | — |
| Description | text | — |
| Location | text | — |
| Start | date-time | — |
| End | date-time | — |
| Recurrence | text-array | — |
| Recurring event ID | text | — |
| Original start time | object | — |
| Date time | date-time | — |
| Time zone | text | — |
| Visibility | text | — |
| Reminders | object | — |
| Use default | boolean | — |
| Overrides | array | — |
| Show me as | text | — |
| Hangout link | text | — |
| Sequence | integer | — |
| Guests can modify | boolean | — |
| Guests can see other guests | boolean | — |
| Attendees | array | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Response status | text | — |
| Comment | text | — |
| List size | integer | — |
| List index | integer | — |
| Creator | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Organizer | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Attachments | array | — |
| File URL | text | — |
| Title | text | — |
| Mime type | text | — |
| Icon link | text | — |
| File ID | text | — |
| List size | integer | — |
| List index | integer | — |

### list_calendars_public (List calendars)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Minimum access role | text | - | No | — |
| Show deleted | text | - | No | — |
| Show hidden | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Items | array | — |
| Kind | text | — |
| Etag | text | — |
| ID | text | — |
| Summary | text | — |
| Description | text | — |
| Time zone | text | — |
| Color ID | text | — |
| Background color | text | — |
| Foreground color | text | — |
| Selected | boolean | — |
| Access role | text | — |
| Default reminders | array | — |
| Notification settings | object | — |
| Primary | boolean | — |
| Conference properties | object | — |
| List size | integer | — |
| List index | integer | — |

### search_events (Search events)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Calendar ID | text | Yes | Yes | The calendar to search for events in. Click calendar settings in the drop down menu next to the specific calendar. Get calendar ID from calendar address field. |
| Search terms | text | - | Yes | Input terms in the event name or description. Partial matches are returned. |
| Single events | text | - | Yes | Set this to Yes to receive each occurrence of a recurring event as an individual event. |
| Date from | date-time | - | Yes | Fetch events starting on or after this datetime |
| Date to | date-time | - | Yes | Fetch events ending on or before this datetime |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Events | array | — |
| Kind | text | — |
| Etag | text | — |
| Color ID | text | — |
| Event import ID | text | — |
| ID | text | — |
| Status | text | — |
| URL | text | — |
| Created | date-time | — |
| Updated | date-time | — |
| Summary | text | — |
| Description | text | — |
| Location | text | — |
| Start | date-time | — |
| End | date-time | — |
| Recurrence | text-array | — |
| Recurring event ID | text | — |
| Original start time | object | — |
| Visibility | text | — |
| Reminders | object | — |
| Show me as | text | — |
| Hangout link | text | — |
| Sequence | integer | — |
| Guests can modify | boolean | — |
| Guests can see other guests | boolean | — |
| Attachments | array | — |
| Attendees | array | — |
| Creator | object | — |
| Organizer | object | — |
| List size | integer | — |
| List index | integer | — |

### update_event (Update event)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Event ID | text | Yes | Yes | Obtain event ID from the Search events action. You can also obtain the event ID from your event URL. |
| Start date time | date-time | - | Yes | Event start date and time |
| End date time | date-time | - | Yes | Event end date and time |
| Name | text | - | Yes | Event name or summary |
| Send notifications? | text | - | Yes | This field is deprecated. This field will be overridden by send updates field. If true, sends notifications about created or updated events. |
| Calendar | text | - | No | — |
| Displayed time zone | text | - | No | — |
| Event description | text | - | No | — |
| Location | text | - | No | — |
| Attendee emails | text | - | No | — |
| Send updates | text | - | No | — |
| Guests can modify? | text | - | No | — |
| Display guests list? | text | - | No | — |
| Status | text | - | No | — |
| Visibility | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| Kind | text | — |
| Etag | text | — |
| Color ID | text | — |
| Event import ID | text | — |
| ID | text | — |
| Status | text | — |
| URL | text | — |
| Created | date-time | — |
| Updated | date-time | — |
| Summary | text | — |
| Description | text | — |
| Location | text | — |
| Start | date-time | — |
| End | date-time | — |
| Recurrence | text-array | — |
| Recurring event ID | text | — |
| Original start time | object | — |
| Date time | date-time | — |
| Time zone | text | — |
| Visibility | text | — |
| Reminders | object | — |
| Use default | boolean | — |
| Overrides | array | — |
| Show me as | text | — |
| Hangout link | text | — |
| Sequence | integer | — |
| Guests can modify | boolean | — |
| Guests can see other guests | boolean | — |
| Attendees | array | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Response status | text | — |
| Comment | text | — |
| List size | integer | — |
| List index | integer | — |
| Creator | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Organizer | object | — |
| ID | text | — |
| Email | text | — |
| Name | text | — |
| Self | boolean | — |
| Attachments | array | — |
| File URL | text | — |
| Title | text | — |
| Mime type | text | — |
| Icon link | text | — |
| File ID | text | — |
| List size | integer | — |
| List index | integer | — |

### update_task (Update task)

Kind: Action
Learned from: `/auto-learn` (UI observation) — 2026-04-27

#### Input fields
| Field | Type | Required | Visible by default | Description |
|---|---|---|---|---|
| Tasklist |  | Yes | Yes | — |
| Task ID | text | Yes | Yes | — |
| Notes | text | - | No | — |
| Status | text | - | No | — |
| Due date | date-time | - | No | — |
| Completed date | date-time | - | No | — |
| Hidden | text | - | No | — |

#### Output fields
| Field | Type | Description |
|---|---|---|
| ID | text | — |
| Etag | text | — |
| Parent | text | — |
| Title | text | — |
| Description | text | — |
| Status | text | — |
| Position | text | — |
| Self link | text | — |
| Updated | date-time | — |
| Due date | date-time | — |
| Completed date | date-time | — |
| Hidden | boolean | — |
| Deleted | boolean | — |
| Links | array | — |
| Type | text | — |
| Description | text | — |
| Link | text | — |
| List size | integer | — |
| List index | integer | — |

---


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
