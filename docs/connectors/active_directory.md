# Active Directory コネクタ

Provider: `active_directory`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New entry | `new_entry` | - |  |
| Scheduled entry search using search filter | `paged_search_entries` | Yes |  |
| New/updated entry | `updated_entry` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Add entry | `add_entry` | - |  |
| Add group | `add_group` | - |  |
| Add user | `add_user` | - |  |
| Add user to group | `add_user_to_group` | - |  |
| Delete entry | `delete_entry` | - |  |
| Disable a user account | `disable_user` | - |  |
| Move user to Organizational unit | `move_user_to_ou` | - |  |
| Remove user from group | `remove_user_from_group` | - |  |
| Rename entry | `rename_entry` | - |  |
| Search entries | `search_entries` | Yes |  |
| Search groups | `search_groups` | Yes |  |
| Search users | `search_users` | Yes |  |
| Set password to User | `set_password` | - |  |
| Update entry | `update_entry` | - |  |
| Update user | `update_user` | - |  |
