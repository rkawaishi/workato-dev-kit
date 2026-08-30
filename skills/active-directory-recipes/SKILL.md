# Active Directory recipes

Provider value to use in every step: `active_directory`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "active_directory"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- This connector has no custom-action escape hatch; if no native operation fits, use the HTTP connector instead.

## Triggers (3)

| Internal name | Title | Batch |
|---|---|---|
| `new_entry` | New entry | - |
| `paged_search_entries` | Scheduled entry search using search filter | yes |
| `updated_entry` | New/updated entry | - |


## Actions (15)

| Internal name | Title | Batch |
|---|---|---|
| `add_entry` | Add entry | - |
| `add_group` | Add group | - |
| `add_user` | Add user | - |
| `add_user_to_group` | Add user to group | - |
| `delete_entry` | Delete entry | - |
| `disable_user` | Disable a user account | - |
| `move_user_to_ou` | Move user to Organizational unit | - |
| `remove_user_from_group` | Remove user from group | - |
| `rename_entry` | Rename entry | - |
| `search_entries` | Search entries | yes |
| `search_groups` | Search groups | yes |
| `search_users` | Search users | yes |
| `set_password` | Set password to User | - |
| `update_entry` | Update entry | - |
| `update_user` | Update user | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
