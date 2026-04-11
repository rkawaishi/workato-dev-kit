# Okta secondary コネクタ

Provider: `okta_secondary`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New events | `new_events` | - |  |
| New events | `new_events_hook` | - |  |
| Scheduled event search using filter | `scheduled_new_events` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Activate user | `activate_people` | - |  |
| Add user to group | `add_user_to_group` | - |  |
| Create user | `create_people` | - |  |
| Deactivate user | `deactivate_people` | - |  |
| Delete user | `delete_people` | - |  |
| Expire an existing user password | `expire_user_password` | - |  |
| Get group members | `get_group_members` | Yes |  |
| Get groups by name | `get_groups_by_name` | Yes |  |
| Get user by ID | `get_people_by_id` | - |  |
| Get user groups | `get_people_groups` | Yes |  |
| Get recent log on events by IP address | `get_recent_logon_events_by_ip_address` | Yes |  |
| Get recent log on events by user | `get_recent_logon_events_by_user` | Yes |  |
| List applications assigned to user | `list_applications_assigned_to_people` | Yes |  |
| Remove user from group | `remove_user_from_group` | - |  |
| Reset forgotten user password | `reset_forgotten_user_password` | - |  |
| Reset MFA factors for user | `reset_user_mfa` | - |  |
| Reset user password | `reset_user_password` | - |  |
| Search Users | `search_users` | Yes |  |
| Suspend user | `suspend_user` | - |  |
| Unsuspend user | `unsuspend_user` | - |  |
| Update user | `update_people` | - |  |
