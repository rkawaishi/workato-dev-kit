# HubSpot コネクタ

Provider: `hubspot`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New company | `new_company` | - |  [deprecated] |
| New contact | `new_contact` | - |  [deprecated] |
| New contact in contact list | `new_contact_in_list` | - |  [deprecated] |
| New contact in list | `new_contact_in_list_v3` | - |  |
| New contact | `new_contact_v2` | - |  [deprecated] |
| New form submission | `new_form_submission` | - |  |
| New record | `new_object` | - |  |
| New records | `new_object_batch` | Yes |  |
| New/updated company | `new_or_updated_company` | - |  [deprecated] |
| New/updated contacts | `new_or_updated_contact` | - |  [deprecated] |
| New/updated deal | `new_or_updated_deal` | - |  [deprecated] |
| New/updated record | `new_or_updated_object` | - |  |
| New/updated records | `new_or_updated_object_batch` | Yes |  |
| New/updated records | `updated_object_batch` | Yes |  [deprecated] |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Add contact to list | `add_contact_to_list` | - |  [deprecated] |
| Add contact to list | `add_contact_to_list_v3` | Yes |  |
| Add contact to workflow | `add_contact_to_workflow` | - |  |
| Associate records | `associate_records` | - |  |
| Associate records | `associate_records_batch` | Yes |  |
| Import CRM Data | `bulk_import_crm` | - |  |
| Create company | `create_company` | - |  [deprecated] |
| Create contact | `create_contact` | - |  [deprecated] |
| Create deal | `create_deal` | - |  [deprecated] |
| Create engagement | `create_engagement` | - |  |
| Create record | `create_object` | - |  |
| Create records | `create_object_batch` | Yes |  |
| Create/update contact | `create_or_update_contact` | - |  [deprecated] |
| Delete associations | `delete_associations` | Yes |  |
| Delete contact | `delete_contact` | - |  |
| Export object data | `export_file` | - |  |
| Get associations | `get_associations` | Yes |  |
| Get company details by ID | `get_company_by_id` | - |  [deprecated] |
| Get contact details by email | `get_contact_by_email` | - |  [deprecated] |
| Get contact details by VID | `get_contact_by_id` | - |  [deprecated] |
| Get contacts associated with a company | `get_contacts_at_a_company` | Yes |  |
| Get contacts in contact list | `get_contacts_in_contact_list` | Yes |  [deprecated] |
| Get contacts in list | `get_contacts_in_list_v3` | Yes |  |
| Get deal by ID | `get_deal_by_id` | - |  [deprecated] |
| Get owner details | `get_owner` | - |  |
| Get owner details by ID | `get_owner_v3` | - |  |
| Get record | `get_record` | - |  |
| List associations | `list_associations` | Yes |  |
| Remove contact from contact list  | `remove_contact_from_contact_list` | Yes |  [deprecated] |
| Remove contact from list | `remove_contact_from_list_v3` | Yes |  |
| Search for companies | `search_companies` | - |  [deprecated] |
| Search contacts | `search_contacts` | - |  [deprecated] |
| Search pipeline stages | `search_pipeline_stages` | Yes |  |
| Search record | `search_record` | Yes |  |
| Update company | `update_company` | - |  [deprecated] |
| Update deal | `update_deal` | - |  [deprecated] |
| Update record | `update_object` | - |  |
| Update records | `update_object_batch` | Yes |  |
