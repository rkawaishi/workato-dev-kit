# Zoho CRM recipes

Provider value to use in every step: `zohocrm`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "zohocrm"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (19)

| Internal name | Title | Batch |
|---|---|---|
| `new_account` | New account | - |
| `new_call` | New call | - |
| `new_case` | New case | - |
| `new_contact` | New contact | - |
| `new_invoice` | New invoice | - |
| `new_object_custom` | New custom object | - |
| `new_object_standard` | New standard object | - |
| `new_potential` | New deal | - |
| `new_updated_contacts_batch` | New/updated Contacts | yes |
| `new_updated_leads_batch` | New/updated Leads | yes |
| `new_vendor` | New vendor | - |
| `update_object_custom` | New/updated custom object | - |
| `update_object_standard` | New/updated standard object | - |
| `updated_account` | New or updated account | - |
| `updated_call` | New or updated call | - |
| `updated_case` | New or updated case | - |
| `updated_contact` | New or updated contact | - |
| `updated_lead` | New or updated lead | - |
| `updated_potential` | New or updated deal | - |


## Actions (45)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_member_to_campaign` | Relate a member to campaign | - |
| `batch_create_objects_custom` | Batch create custom objects | yes |
| `batch_create_objects_standard` | Batch create standard objects | yes |
| `batch_update_objects_custom` | Batch update custom objects | yes |
| `batch_update_objects_standard` | Batch update standard objects | yes |
| `batch_upsert_objects_custom` | Batch upsert custom objects | yes |
| `batch_upsert_objects_standard` | Batch upsert standard objects | yes |
| `bulk_create_objects_custom` | Bulk create custom objects | - |
| `bulk_create_objects_standard` | Bulk create standard objects | - |
| `bulk_update_objects_custom` | Bulk update custom objects | - |
| `bulk_update_objects_standard` | Bulk update standard objects | - |
| `bulk_upsert_objects_custom` | Bulk upsert custom objects | - |
| `bulk_upsert_objects_standard` | Bulk upsert standard objects | - |
| `coql_search` | Search records using COQL query | - |
| `create_account` | Create account | - |
| `create_campaign` | Create campaign | - |
| `create_contact` | Create contact | - |
| `create_invoice` | Create invoice | - |
| `create_lead` | Create lead | - |
| `create_potential` | Create deal | - |
| `create_vendor` | Create vendor | - |
| `delete_object_custom` | Delete custom object | - |
| `delete_object_standard` | Delete standard object | - |
| `get_lead_by_id` | Get lead by ID | - |
| `get_object_by_id` | Get object by ID | - |
| `search_account` | Search accounts | yes |
| `search_campaigns` | Search campaigns | yes |
| `search_contact` | Search contacts | yes |
| `search_invoice` | Search invoice | - |
| `search_lead` | Search leads | yes |
| `search_objects_custom` | Search custom objects | - |
| `search_objects_standard` | Search standard objects | - |
| `search_potential` | Search deals | yes |
| `search_product` | Search products | yes |
| `search_vendor` | Search vendors | yes |
| `update_account` | Update account | - |
| `update_campaign` | Update campaign | - |
| `update_contact` | Update contact | - |
| `update_invoice` | Update invoice | - |
| `update_lead` | Update lead | - |
| `update_potential` | Update deal | - |
| `update_vendor` | Update vendor | - |
| `upsert_object_custom` | Upsert custom object | - |
| `upsert_object_standard` | Upsert standard object | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
