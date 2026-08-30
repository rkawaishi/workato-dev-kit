# HubSpot recipes

Provider value to use in every step: `hubspot`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "hubspot"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (6)

| Internal name | Title | Batch |
|---|---|---|
| `new_contact_in_list_v3` | New contact in list | - |
| `new_form_submission` | New form submission | - |
| `new_object` | New record | - |
| `new_object_batch` | New records | yes |
| `new_or_updated_object` | New/updated record | - |
| `new_or_updated_object_batch` | New/updated records | yes |


## Actions (24)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_contact_to_list_v3` | Add contact to list | yes |
| `add_contact_to_workflow` | Add contact to workflow | - |
| `associate_records` | Associate records | - |
| `associate_records_batch` | Associate records | yes |
| `bulk_import_crm` | Import CRM Data | - |
| `create_engagement` | Create engagement | - |
| `create_object` | Create record | - |
| `create_object_batch` | Create records | yes |
| `delete_associations` | Delete associations | yes |
| `delete_contact` | Delete contact | - |
| `export_file` | Export object data | - |
| `get_associations` | Get associations | yes |
| `get_contacts_at_a_company` | Get contacts associated with a company | yes |
| `get_contacts_in_list_v3` | Get contacts in list | yes |
| `get_owner` | Get owner details | - |
| `get_owner_v3` | Get owner details by ID | - |
| `get_record` | Get record | - |
| `list_associations` | List associations | yes |
| `remove_contact_from_list_v3` | Remove contact from list | yes |
| `search_pipeline_stages` | Search pipeline stages | yes |
| `search_record` | Search record | yes |
| `update_object` | Update record | - |
| `update_object_batch` | Update records | yes |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `new_company` | New company | - |
| `new_contact` | New contact | - |
| `new_contact_in_list` | New contact in contact list | - |
| `new_contact_v2` | New contact | - |
| `new_or_updated_company` | New/updated company | - |
| `new_or_updated_contact` | New/updated contacts | - |
| `new_or_updated_deal` | New/updated deal | - |
| `updated_object_batch` | New/updated records | yes |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `add_contact_to_list` | Add contact to list | - |
| `create_company` | Create company | - |
| `create_contact` | Create contact | - |
| `create_deal` | Create deal | - |
| `create_or_update_contact` | Create/update contact | - |
| `get_company_by_id` | Get company details by ID | - |
| `get_contact_by_email` | Get contact details by email | - |
| `get_contact_by_id` | Get contact details by VID | - |
| `get_contacts_in_contact_list` | Get contacts in contact list | yes |
| `get_deal_by_id` | Get deal by ID | - |
| `remove_contact_from_contact_list` | Remove contact from contact list | yes |
| `search_companies` | Search for companies | - |
| `search_contacts` | Search contacts | - |
| `update_company` | Update company | - |
| `update_deal` | Update deal | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
