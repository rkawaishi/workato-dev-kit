# Zendesk recipes

Provider value to use in every step: `zendesk`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "zendesk"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (9)

| Internal name | Title | Batch |
|---|---|---|
| `new_organization` | New organization | - |
| `new_ticket_polling` | New ticket | - |
| `new_ticket_webhook` | New ticket | - |
| `new_updated_object_batch` | New/updated records | yes |
| `new_user` | New user | - |
| `updated_organization` | New/updated organization | - |
| `updated_ticket_polling` | New/updated ticket | - |
| `updated_ticket_webhook` | New/updated ticket | - |
| `updated_user` | New/updated user | - |


## Actions (33)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_organization_member` | Create organization membership | - |
| `bulk_ticket_update` | Bulk update tickets | - |
| `bulk_upsert` | Create/update records | yes |
| `close_ticket` | Solve ticket | - |
| `create_custom_record` | Create custom object record | - |
| `create_organization` | Create organization | - |
| `create_relationship_record` | Create relationship record | - |
| `create_ticket` | Create ticket | - |
| `create_upload` | Upload attachment | - |
| `create_user` | Create user | - |
| `delete_custom_record` | Delete custom object record by ID | - |
| `delete_relation_record` | Delete relationship record by ID | - |
| `delete_ticket` | Delete ticket | - |
| `get_custom_record` | Get custom object record by ID | - |
| `get_organization_by_id` | Get organization details by ID | - |
| `get_orgs_by_external_ids` | Get organizations by external IDs | yes |
| `get_relationship_records` | Get relationship record(s) | yes |
| `get_ticket_by_id` | Get ticket details by ID | - |
| `get_ticket_comments` | Get comments for ticket | yes |
| `get_tickets_by_external_id` | Get list of tickets by external IDs | yes |
| `get_user_by_id` | Get user details by ID | - |
| `list_custom_record` | Get list of custom object records by external IDs | yes |
| `list_user_identities` | List user identities | yes |
| `lookup_group` | Get group by name | - |
| `lookup_organization_member` | Search organization member | yes |
| `search_organization` | Search organizations | yes |
| `search_ticket` | Search tickets | yes |
| `search_user` | Search users | yes |
| `update_custom_record` | Update custom object record | - |
| `update_organization` | Update organization | - |
| `update_ticket` | Update ticket | - |
| `update_user` | Update user | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_ticket` | New ticket | - |
| `updated_object_batch` | New/updated records | yes |
| `updated_ticket` | New/updated ticket | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
