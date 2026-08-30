# Eventbrite recipes

Provider value to use in every step: `event_brite`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "event_brite"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (7)

| Internal name | Title | Batch |
|---|---|---|
| `new_contact` | New contact created | - |
| `new_user_event` | New event created | - |
| `new_user_event_attendee` | New attendee registered for event | - |
| `new_user_event_order` | New order for event | - |
| `updated_user_event_attendee` | New/updated attendee registered for event | - |
| `updated_user_event_attendee_webhook` | New/updated attendee registered for event | - |
| `updated_user_event_order` | New/updated order for event | - |


## Actions (5)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_contact` | Create/update contact | - |
| `create_contact_list` | Create contact list | - |
| `get_attendees` | Get event attendees | yes |
| `search_events` | Search events | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
