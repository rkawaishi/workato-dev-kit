# Basecamp 2 recipes

Provider value to use in every step: `basecamp`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "basecamp"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (9)

| Internal name | Title | Batch |
|---|---|---|
| `calendar_access_granted` | Access granted to calendar | - |
| `new_calendar_event` | New calendar event | - |
| `new_people_event` | New person event | - |
| `new_project` | New project | - |
| `new_project_calendar_event` | New project calendar event | - |
| `new_project_event` | New project event | - |
| `new_todo` | New to-do | - |
| `new_todolist` | New to-do list | - |
| `project_access_granted` | Access granted to project | - |


## Actions (9)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `create_calendar_event` | Create calendar event | - |
| `create_project` | Create new project | - |
| `create_project_calendar_event` | Create project calendar event | - |
| `create_todo` | Create new todo | - |
| `create_todolist` | Create new to-do list | - |
| `lookup_calendar` | Search calendars | - |
| `lookup_person` | Search persons | - |
| `lookup_project` | Search projects | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
