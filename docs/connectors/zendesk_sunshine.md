# Zendesk Sunshine コネクタ

Provider: `zendesk_sunshine`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New organization | `new_organization` | - |  |
| New ticket | `new_ticket` | - |  [deprecated] |
| New ticket | `new_ticket_polling` | - |  |
| New ticket | `new_ticket_webhook` | - |  |
| New/updated records | `new_updated_object_batch` | Yes |  |
| New user | `new_user` | - |  |
| New/updated records | `updated_object_batch` | Yes |  [deprecated] |
| New/updated organization | `updated_organization` | - |  |
| New/updated ticket | `updated_ticket` | - |  [deprecated] |
| New/updated ticket | `updated_ticket_polling` | - |  |
| New/updated ticket | `updated_ticket_webhook` | - |  |
| New/updated user | `updated_user` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create organization membership | `add_organization_member` | - |  |
| Bulk update tickets | `bulk_ticket_update` | - |  |
| Create/update records | `bulk_upsert` | Yes |  |
| Solve ticket | `close_ticket` | - |  |
| Create custom object record | `create_custom_record` | - |  |
| Create organization | `create_organization` | - |  |
| Create relationship record | `create_relationship_record` | - |  |
| Create ticket | `create_ticket` | - |  |
| Upload attachment | `create_upload` | - |  |
| Create user | `create_user` | - |  |
| Delete custom object record by ID | `delete_custom_record` | - |  |
| Delete relationship record by ID | `delete_relation_record` | - |  |
| Delete ticket | `delete_ticket` | - |  |
| Get custom object record by ID | `get_custom_record` | - |  |
| Get organization details by ID | `get_organization_by_id` | - |  |
| Get organizations by external IDs | `get_orgs_by_external_ids` | Yes |  |
| Get relationship record(s) | `get_relationship_records` | Yes |  |
| Get ticket details by ID | `get_ticket_by_id` | - |  |
| Get comments for ticket | `get_ticket_comments` | Yes |  |
| Get list of tickets by external IDs | `get_tickets_by_external_id` | Yes |  |
| Get user details by ID | `get_user_by_id` | - |  |
| Get list of custom object records by external IDs | `list_custom_record` | Yes |  |
| List user identities | `list_user_identities` | Yes |  |
| Get group by name | `lookup_group` | - |  |
| Search organization member | `lookup_organization_member` | Yes |  |
| Search organizations | `search_organization` | Yes |  |
| Search tickets | `search_ticket` | Yes |  |
| Search users | `search_user` | Yes |  |
| Update custom object record | `update_custom_record` | - |  |
| Update organization | `update_organization` | - |  |
| Update ticket | `update_ticket` | - |  |
| Update user | `update_user` | - |  |
