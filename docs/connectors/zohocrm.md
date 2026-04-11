# Zoho CRM コネクタ

Provider: `zohocrm`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New account | `new_account` | - |  |
| New call | `new_call` | - |  |
| New case | `new_case` | - |  |
| New contact | `new_contact` | - |  |
| New invoice | `new_invoice` | - |  |
| New custom object | `new_object_custom` | - |  |
| New standard object | `new_object_standard` | - |  |
| New deal | `new_potential` | - |  |
| New/updated Contacts | `new_updated_contacts_batch` | Yes |  |
| New/updated Leads | `new_updated_leads_batch` | Yes |  |
| New vendor | `new_vendor` | - |  |
| New/updated custom object | `update_object_custom` | - |  |
| New/updated standard object | `update_object_standard` | - |  |
| New or updated account | `updated_account` | - |  |
| New or updated call | `updated_call` | - |  |
| New or updated case | `updated_case` | - |  |
| New or updated contact | `updated_contact` | - |  |
| New or updated lead | `updated_lead` | - |  |
| New or updated deal | `updated_potential` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Relate a member to campaign | `add_member_to_campaign` | - |  |
| Batch create custom objects | `batch_create_objects_custom` | Yes |  |
| Batch create standard objects | `batch_create_objects_standard` | Yes |  |
| Batch update custom objects | `batch_update_objects_custom` | Yes |  |
| Batch update standard objects | `batch_update_objects_standard` | Yes |  |
| Batch upsert custom objects | `batch_upsert_objects_custom` | Yes |  |
| Batch upsert standard objects | `batch_upsert_objects_standard` | Yes |  |
| Bulk create custom objects | `bulk_create_objects_custom` | - |  |
| Bulk create standard objects | `bulk_create_objects_standard` | - |  |
| Bulk update custom objects | `bulk_update_objects_custom` | - |  |
| Bulk update standard objects | `bulk_update_objects_standard` | - |  |
| Bulk upsert custom objects | `bulk_upsert_objects_custom` | - |  |
| Bulk upsert standard objects | `bulk_upsert_objects_standard` | - |  |
| Search records using COQL query | `coql_search` | - |  |
| Create account | `create_account` | - |  |
| Create campaign | `create_campaign` | - |  |
| Create contact | `create_contact` | - |  |
| Create invoice | `create_invoice` | - |  |
| Create lead | `create_lead` | - |  |
| Create deal | `create_potential` | - |  |
| Create vendor | `create_vendor` | - |  |
| Delete custom object | `delete_object_custom` | - |  |
| Delete standard object | `delete_object_standard` | - |  |
| Get lead by ID | `get_lead_by_id` | - |  |
| Get object by ID | `get_object_by_id` | - |  |
| Search accounts | `search_account` | Yes |  |
| Search campaigns | `search_campaigns` | Yes |  |
| Search contacts | `search_contact` | Yes |  |
| Search invoice | `search_invoice` | - |  |
| Search leads | `search_lead` | Yes |  |
| Search custom objects | `search_objects_custom` | - |  |
| Search standard objects | `search_objects_standard` | - |  |
| Search deals | `search_potential` | Yes |  |
| Search products | `search_product` | Yes |  |
| Search vendors | `search_vendor` | Yes |  |
| Update account | `update_account` | - |  |
| Update campaign | `update_campaign` | - |  |
| Update contact | `update_contact` | - |  |
| Update invoice | `update_invoice` | - |  |
| Update lead | `update_lead` | - |  |
| Update deal | `update_potential` | - |  |
| Update vendor | `update_vendor` | - |  |
| Upsert custom object | `upsert_object_custom` | - |  |
| Upsert standard object | `upsert_object_standard` | - |  |
