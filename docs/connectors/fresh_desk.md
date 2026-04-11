# Freshdesk コネクタ

Provider: `fresh_desk`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Closed ticket | `closed_ticket` | - |  |
| Company created | `company_created` | - |  |
| Company updated | `company_updated` | - |  |
| New ticket | `new_ticket` | - |  [deprecated] |
| New/updated ticket | `new_updated_ticket_v2` | - |  |
| Updated ticket | `updated_ticket` | - |  [deprecated] |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add note to ticket | `add_note_to_ticket` | - |  |
| Create company | `create_company` | - |  |
| Create contact | `create_contact` | - |  |
| Create ticket | `create_ticket` | - |  |
| Get agent details | `get_agent` | - |  |
| Get group details by ID | `get_group_by_id` | - |  |
| Get ticket by ID | `get_ticket` | - |  |
| Get ticket attachments | `get_ticket_attachments` | - |  |
| Get user details | `get_user` | - |  |
| Search companies | `search_companies` | Yes |  [deprecated] |
| Search companies | `search_companies_v2` | Yes |  |
| Search users | `search_contacts` | Yes |  [deprecated] |
| Search contacts | `search_contacts_v2` | Yes |  |
| Search tickets | `search_tickets` | Yes |  |
| Update company | `update_company` | - |  |
| Update contact | `update_contact` | - |  |
| Update ticket | `update_ticket` | - |  [deprecated] |
| Update ticket | `update_ticket_v2` | - |  |
