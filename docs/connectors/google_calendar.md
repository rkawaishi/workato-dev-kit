# Google Calendar コネクタ

Provider: `google_calendar`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Event end | `event_end` | - |  |
| Event start | `event_start` | - |  |
| New event | `new_event` | - |  |
| New/updated event | `updated_event` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add attendees to an event | `add_attendee_to_an_event` | Yes |  |
| Create all day event | `create_allday_event` | - |  |
| Create calendar | `create_calendar` | - |  |
| Create event | `create_event` | - |  |
| Create task | `create_task` | - |  |
| Delete attendees from an event | `delete_attendees_from_an_event` | Yes |  |
| Delete event | `delete_event` | - |  |
| Get calendar by ID | `get_calendar_by_id` | - |  |
| Get event by ID | `get_event_by_id` | - |  |
| List calendars | `list_calendars_public` | - |  |
| Search events | `search_events` | Yes |  |
| Update event | `update_event` | - |  |
| Update task | `update_task` | - |  |

## フィールド詳細

### event_end (Event end)

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select a calendar to monitor for event end. |
| Search term | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
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

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select a calendar to monitor for event start. |
| Time before unit |  | Yes | Yes | Select a time unit for Time before event start. |
| Time before event start | integer | Yes | Yes | Enter the time before the event start you want the trigger to pick up the event. The minimum allowed duration is 5 minutes. |
| Search term | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
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

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select a calendar to monitor for events |
| Include deleted events? | text | - | Yes | When set to true, job will be triggered for deleted events also. Defaults to false |

#### Output fields
| フィールド | 型 | 説明 |
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

種別: Trigger
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select a calendar to monitor for events |
| Include deleted events? | text | - | Yes | When set to true, job will be triggered for deleted events also. Defaults to false |

#### Output fields
| フィールド | 型 | 説明 |
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

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select calendar that event belongs to |
| Event ID | text | Yes | Yes | Obtain event ID from the Search events action. You can also obtain the event ID from your event URL. |
| Attendees | array | Yes | Yes | — |
| Send notifications? | text | - | Yes | If true, will notify all attendees about changed event |
| Comment | text | - | No | — |
| Optional | text | - | No | — |
| Response status | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
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

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
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
| フィールド | 型 | 説明 |
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

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Calendar name | text | Yes | Yes | — |
| Description | text | - | No | — |
| Time zone | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
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

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
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
| フィールド | 型 | 説明 |
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

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Tasklist |  | Yes | Yes | — |
| Task name | text | Yes | Yes | — |
| Notes | text | - | No | — |
| Status | text | - | No | — |
| Due date | date-time | - | No | — |
| Completed date | date-time | - | No | — |
| Hidden | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
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

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select calendar that event belongs to |
| Event ID | text | Yes | Yes | Obtain event ID from the Search events action. You can also obtain the event ID from your event URL. |
| Attendees | array | Yes | Yes | List of attendees to delete |
| Send notifications? | text | - | Yes | If true, will notify all attendees about changed event |

#### Output fields
| フィールド | 型 | 説明 |
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

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

> ⚠ 部分学習: 出力スキーマなし (fire-and-forget action)

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Calendar |  | Yes | Yes | Select calendar that event belongs to |
| Event ID | text | Yes | Yes | Obtain event ID from the Search events action. You can also obtain the event ID from your event URL. |
| Send notification? | text | - | Yes | If true, will notify attendees about event being deleted |

### get_calendar_by_id (Get calendar by ID)

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Calendar ID | text | Yes | Yes | — |

#### Output fields
| フィールド | 型 | 説明 |
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

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Calendar ID | text | Yes | Yes | ID of calendar that event belongs to. Click calendar settings in the drop down menu next to the specific calendar. Get calendar ID from calendar address field. |
| Event ID | text | Yes | Yes | Obtain event ID from the Search events action. You can also obtain the event ID from your event URL. |

#### Output fields
| フィールド | 型 | 説明 |
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

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Minimum access role | text | - | No | — |
| Show deleted | text | - | No | — |
| Show hidden | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
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

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Calendar ID | text | Yes | Yes | The calendar to search for events in. Click calendar settings in the drop down menu next to the specific calendar. Get calendar ID from calendar address field. |
| Search terms | text | - | Yes | Input terms in the event name or description. Partial matches are returned. |
| Single events | text | - | Yes | Set this to Yes to receive each occurrence of a recurring event as an individual event. |
| Date from | date-time | - | Yes | Fetch events starting on or after this datetime |
| Date to | date-time | - | Yes | Fetch events ending on or before this datetime |

#### Output fields
| フィールド | 型 | 説明 |
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

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
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
| フィールド | 型 | 説明 |
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

種別: Action
学習元: /auto-learn (UI 観察) — 2026-04-27

#### Input fields
| フィールド | 型 | 必須 | デフォルト表示 | 説明 |
|---|---|---|---|---|
| Tasklist |  | Yes | Yes | — |
| Task ID | text | Yes | Yes | — |
| Notes | text | - | No | — |
| Status | text | - | No | — |
| Due date | date-time | - | No | — |
| Completed date | date-time | - | No | — |
| Hidden | text | - | No | — |

#### Output fields
| フィールド | 型 | 説明 |
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

## 学習サマリ

最終実行: 2026-04-27 by /auto-learn
- 試行: 17 op
- 完全成功: 16
- 部分学習: 1
- 学習失敗: 0
- スキップ:
  - Deprecated: 0
  - adhoc: 1 — `__adhoc_http_action`
  - 既学習: 0

### 要 follow-up

- **Fire-and-forget (UI 仕様・追加学習不要)**
  - `delete_event` — 削除アクション。output_group_not_found

### 構造的注記（参考）

- 重複ラベル `Email`: `Creator` / `Organizer` / `Attendees[]` 配下で出現。データツリー paddingLeft=0 でフラット表示
- `event_start` / `event_end` トリガー: `Conference data` / `Focus time properties` / `Out of office properties` / `Working location properties` を含む 76 フィールドが output に出る（`new_event` / `updated_event` の 56 フィールドより多い）
- 内部 JSON キーと UI label のマッピングは UI 観察では取れない（`/learn-recipe` で補完）
