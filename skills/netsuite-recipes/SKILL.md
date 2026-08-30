# NetSuite SOAP recipes

Provider value to use in every step: `netsuite`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "netsuite"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (24)

| Internal name | Title | Batch |
|---|---|---|
| `created_object_bulk` | Export new standard records | yes |
| `custom_created_object_bulk` | Export new custom records | yes |
| `custom_updated_object_bulk` | Export new/updated custom records | yes |
| `deleted_object` | Deleted standard record | - |
| `new_classification_object` | New classification record | - |
| `new_classification_object_batch` | New classification records | yes |
| `new_classification_saved_search_result` | New classification records in a saved search | - |
| `new_custom_object` | New custom record | - |
| `new_custom_object_batch` | New custom records | yes |
| `new_custom_object_saved_search_result` | New custom records in a saved search | - |
| `new_custom_object_saved_search_result_batch` | New custom records in a saved search | yes |
| `new_object` | New standard record | - |
| `new_object_batch` | New standard records | yes |
| `new_saved_search_result` | New standard records in a saved search | - |
| `new_saved_search_result_batch` | New standard records in a saved search | yes |
| `updated_custom_object` | New/updated custom record | - |
| `updated_custom_object_batch` | New/updated custom records | yes |
| `updated_custom_object_saved_search_result` | New/updated custom records in a saved search | - |
| `updated_custom_object_saved_search_result_batch` | New/updated custom records in a saved search | yes |
| `updated_object` | New/updated standard record | - |
| `updated_object_batch` | New/updated standard records | yes |
| `updated_object_bulk` | Export new/updated standard records | yes |
| `updated_saved_search_result` | New/updated standard records in a saved search | - |
| `updated_saved_search_result_batch` | New/updated standard records in a saved search | yes |


## Actions (37)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `add_custom_batch_job` | Create custom records in batch | yes |
| `add_custom_bulk_job_v2` | Create custom records in bulk | yes |
| `add_custom_object` | Create custom record | - |
| `add_object` | Create standard record | - |
| `add_standard_batch_job` | Create standard records in batch | yes |
| `add_standard_bulk_job_v2` | Create standard records in bulk | yes |
| `attach_contact_to_object` | Attach contact to record | - |
| `attach_file_to_object` | Attach file to record | - |
| `delete_custom_record` | Delete custom record | - |
| `delete_custom_record_batch` | Delete custom records | yes |
| `delete_record` | Delete standard record | - |
| `delete_record_batch` | Delete standard records | yes |
| `execute_custom_saved_search` | Execute saved search for custom record | yes |
| `execute_saved_search` | Execute saved search for record | yes |
| `execute_suiteql` | Execute SuiteQL query | yes |
| `get_all_object` | Get all standard records | yes |
| `get_case_comments` | Get case comments | yes |
| `get_custom_object_schema` | Get object schema for custom record | - |
| `get_file_by_id` | Get file by ID | - |
| `get_posting_transaction_summary` | Get posting transaction summary | - |
| `get_standard_object_schema` | Get object schema for standard record | - |
| `initialize_operation` | Initialize record | - |
| `search_custom_object` | Search custom records | yes |
| `search_object_v2` | Search standard records | yes |
| `update_custom_batch_job` | Update custom records in batch | yes |
| `update_custom_bulk_job_v2` | Update custom records in bulk | yes |
| `update_custom_object` | Update custom record | - |
| `update_object` | Update standard record | - |
| `update_standard_batch_job` | Update standard records in batch | yes |
| `update_standard_bulk_job_v2` | Update standard records in bulk | yes |
| `upsert_custom_batch_job` | Upsert custom records in batch | yes |
| `upsert_custom_bulk_job_v2` | Upsert custom records in bulk | yes |
| `upsert_custom_object` | Upsert custom record | - |
| `upsert_object` | Upsert standard record | - |
| `upsert_standard_batch_job` | Upsert standard records in batch | yes |
| `upsert_standard_bulk_job_v2` | Upsert standard records in bulk | yes |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `add_custom_bulk_job` | Create custom records in bulk | yes |
| `add_standard_bulk_job` | Create standard records in bulk | yes |
| `search_object` | Search standard records (deprecated) | - |
| `update_custom_bulk_job` | Update custom records in bulk | yes |
| `update_standard_bulk_job` | Update standard records in bulk | yes |
| `upsert_custom_bulk_job` | Upsert custom records in bulk | yes |
| `upsert_standard_bulk_job` | Upsert standard records in bulk | yes |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
