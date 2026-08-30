# Freshdesk recipes

Provider value to use in every step: `fresh_desk`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "fresh_desk"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (4)

| Internal name | Title | Batch |
|---|---|---|
| `closed_ticket` | Closed ticket | - |
| `company_created` | Company created | - |
| `company_updated` | Company updated | - |
| `new_updated_ticket_v2` | New/updated ticket | - |


## Actions (16)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_note_to_ticket` | Add note to ticket | - |
| `create_company` | Create company | - |
| `create_contact` | Create contact | - |
| `create_ticket` | Create ticket | - |
| `get_agent` | Get agent details | - |
| `get_group_by_id` | Get group details by ID | - |
| `get_ticket` | Get ticket by ID | - |
| `get_ticket_attachments` | Get ticket attachments | - |
| `get_user` | Get user details | - |
| `search_companies_v2` | Search companies | yes |
| `search_contacts_v2` | Search contacts | yes |
| `search_tickets` | Search tickets | yes |
| `update_company` | Update company | - |
| `update_contact` | Update contact | - |
| `update_ticket_v2` | Update ticket | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_ticket` | New ticket | - |
| `updated_ticket` | Updated ticket | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `search_companies` | Search companies | yes |
| `search_contacts` | Search users | yes |
| `update_ticket` | Update ticket | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
