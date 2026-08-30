# Okta recipes

Provider value to use in every step: `okta`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "okta"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `new_events` | New events | - |
| `new_events_hook` | New events | - |
| `scheduled_new_events` | Scheduled event search using filter | yes |


## Actions (22)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `activate_people` | Activate user | - |
| `add_user_to_group` | Add user to group | - |
| `create_people` | Create user | - |
| `deactivate_people` | Deactivate user | - |
| `delete_people` | Delete user | - |
| `expire_user_password` | Expire an existing user password | - |
| `get_group_members` | Get group members | yes |
| `get_groups_by_name` | Get groups by name | yes |
| `get_people_by_id` | Get user by ID | - |
| `get_people_groups` | Get user groups | yes |
| `get_recent_logon_events_by_ip_address` | Get recent log on events by IP address | yes |
| `get_recent_logon_events_by_user` | Get recent log on events by user | yes |
| `list_applications_assigned_to_people` | List applications assigned to user | yes |
| `remove_user_from_group` | Remove user from group | - |
| `reset_forgotten_user_password` | Reset forgotten user password | - |
| `reset_user_mfa` | Reset MFA factors for user | - |
| `reset_user_password` | Reset user password | - |
| `search_users` | Search Users | yes |
| `suspend_user` | Suspend user | - |
| `unsuspend_user` | Unsuspend user | - |
| `update_people` | Update user | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
