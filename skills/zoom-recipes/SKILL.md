# Zoom recipes

Provider value to use in every step: `zoom`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "zoom"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (1)

| Internal name | Title | Batch |
|---|---|---|
| `new_object_events` | New event | - |


## Actions (20)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_group_member` | Add group members | yes |
| `add_registrant` | Add registrant | - |
| `create_group` | Create group | - |
| `create_user` | Create user | - |
| `delete_object` | Delete object | - |
| `delete_users` | Delete users | - |
| `download_cloud_recording` | Download cloud recording | - |
| `get_object` | Get object by ID | - |
| `get_registrants` | Get registrants | yes |
| `get_user` | Get user | - |
| `get_webinar_participants` | Get webinar attendees | yes |
| `get_webinar_results` | Retrieve webinar results | yes |
| `list_object` | List object | yes |
| `schedule_object` | Schedule meeting or webinar | - |
| `search_object` | Search object | yes |
| `search_users` | Search users | yes |
| `update_object` | Update object | - |
| `update_registrant_status` | Update registrant status | - |
| `update_user` | Update user | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
