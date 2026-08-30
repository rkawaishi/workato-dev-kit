# Pagerduty recipes

Provider value to use in every step: `pagerduty`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "pagerduty"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (2)

| Internal name | Title | Batch |
|---|---|---|
| `new_incident` | New incident | - |
| `new_notification` | New notification | - |


## Actions (7)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_note_to_incident` | Add note to incident | - |
| `get_incident_by_ID` | Get incident by ID | - |
| `list_log_entries` | List log entries | yes |
| `search_incident` | Search incident | yes |
| `send_an_event` | Send an event | - |
| `update_incident` | Update incident | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
