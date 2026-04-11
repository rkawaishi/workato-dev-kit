# NetSuite SOAP secondary コネクタ

Provider: `netsuite_secondary`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Export new standard records | `created_object_bulk` | Yes |  |
| Export new custom records | `custom_created_object_bulk` | Yes |  |
| Export new/updated custom records | `custom_updated_object_bulk` | Yes |  |
| Deleted standard record | `deleted_object` | - |  |
| New classification record | `new_classification_object` | - |  |
| New classification records | `new_classification_object_batch` | Yes |  |
| New classification records in a saved search | `new_classification_saved_search_result` | - |  |
| New custom record | `new_custom_object` | - |  |
| New custom records | `new_custom_object_batch` | Yes |  |
| New custom records in a saved search | `new_custom_object_saved_search_result` | - |  |
| New custom records in a saved search | `new_custom_object_saved_search_result_batch` | Yes |  |
| New standard record | `new_object` | - |  |
| New standard records | `new_object_batch` | Yes |  |
| New standard records in a saved search | `new_saved_search_result` | - |  |
| New standard records in a saved search | `new_saved_search_result_batch` | Yes |  |
| New/updated custom record | `updated_custom_object` | - |  |
| New/updated custom records | `updated_custom_object_batch` | Yes |  |
| New/updated custom records in a saved search | `updated_custom_object_saved_search_result` | - |  |
| New/updated custom records in a saved search | `updated_custom_object_saved_search_result_batch` | Yes |  |
| New/updated standard record | `updated_object` | - |  |
| New/updated standard records | `updated_object_batch` | Yes |  |
| Export new/updated standard records | `updated_object_bulk` | Yes |  |
| New/updated standard records in a saved search | `updated_saved_search_result` | - |  |
| New/updated standard records in a saved search | `updated_saved_search_result_batch` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create custom records in batch | `add_custom_batch_job` | Yes |  |
| Create custom records in bulk | `add_custom_bulk_job` | Yes |  [deprecated] |
| Create custom records in bulk | `add_custom_bulk_job_v2` | Yes |  |
| Create custom record | `add_custom_object` | - |  |
| Create standard record | `add_object` | - |  |
| Create standard records in batch | `add_standard_batch_job` | Yes |  |
| Create standard records in bulk | `add_standard_bulk_job` | Yes |  [deprecated] |
| Create standard records in bulk | `add_standard_bulk_job_v2` | Yes |  |
| Attach contact to record | `attach_contact_to_object` | - |  |
| Attach file to record | `attach_file_to_object` | - |  |
| Delete custom record | `delete_custom_record` | - |  |
| Delete custom records | `delete_custom_record_batch` | Yes |  |
| Delete standard record | `delete_record` | - |  |
| Delete standard records | `delete_record_batch` | Yes |  |
| Execute saved search for custom record | `execute_custom_saved_search` | Yes |  |
| Execute saved search for record | `execute_saved_search` | Yes |  |
| Execute SuiteQL query | `execute_suiteql` | Yes |  |
| Get all standard records | `get_all_object` | Yes |  |
| Get case comments | `get_case_comments` | Yes |  |
| Get object schema for custom record | `get_custom_object_schema` | - |  |
| Get file by ID | `get_file_by_id` | - |  |
| Get posting transaction summary | `get_posting_transaction_summary` | - |  |
| Get object schema for standard record | `get_standard_object_schema` | - |  |
| Initialize record | `initialize_operation` | - |  |
| Search custom records | `search_custom_object` | Yes |  |
| Search standard records (deprecated) | `search_object` | - |  [deprecated] |
| Search standard records | `search_object_v2` | Yes |  |
| Update custom records in batch | `update_custom_batch_job` | Yes |  |
| Update custom records in bulk | `update_custom_bulk_job` | Yes |  [deprecated] |
| Update custom records in bulk | `update_custom_bulk_job_v2` | Yes |  |
| Update custom record | `update_custom_object` | - |  |
| Update standard record | `update_object` | - |  |
| Update standard records in batch | `update_standard_batch_job` | Yes |  |
| Update standard records in bulk | `update_standard_bulk_job` | Yes |  [deprecated] |
| Update standard records in bulk | `update_standard_bulk_job_v2` | Yes |  |
| Upsert custom records in batch | `upsert_custom_batch_job` | Yes |  |
| Upsert custom records in bulk | `upsert_custom_bulk_job` | Yes |  [deprecated] |
| Upsert custom records in bulk | `upsert_custom_bulk_job_v2` | Yes |  |
| Upsert custom record | `upsert_custom_object` | - |  |
| Upsert standard record | `upsert_object` | - |  |
| Upsert standard records in batch | `upsert_standard_batch_job` | Yes |  |
| Upsert standard records in bulk | `upsert_standard_bulk_job` | Yes |  [deprecated] |
| Upsert standard records in bulk | `upsert_standard_bulk_job_v2` | Yes |  |
