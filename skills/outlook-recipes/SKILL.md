# Outlook recipes

Provider value to use in every step: `outlook`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "outlook"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (7)

| Internal name | Title | Batch |
|---|---|---|
| `delete_deleted_event` | Deleted event | - |
| `new_contact` | New contact | - |
| `new_email` | New email | - |
| `new_event_v2` | New event | - |
| `new_updated_contact` | New/updated contact | - |
| `updated_email` | New/updated email | - |
| `updated_event` | New/updated event | - |


## Actions (19)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_calendar` | Create calendar | - |
| `create_contact` | Create contact | - |
| `create_event` | Create calendar event | - |
| `delete_calendar_event` | Delete calendar event | - |
| `delete_contact` | Delete contact | - |
| `get_attachments` | Download email attachments | - |
| `get_calendar` | Get calendar by ID | - |
| `get_contact` | Get contact | - |
| `get_event` | Get calendar event by ID | - |
| `list_calendars_outlook` | List calendars | - |
| `list_contact` | List contacts | yes |
| `list_event_instances` | List all instances of an event | yes |
| `search_calendar` | Search calendar | yes |
| `search_contact` | Search contacts | yes |
| `search_events` | Search calendar events | yes |
| `send_mail` | Send email | - |
| `update_contact` | Update contact | - |
| `update_event` | Update calendar event | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_event` | New event | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
