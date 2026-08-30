# Oracle Fusion Cloud recipes

Provider value to use in every step: `oracle_fusion_cloud`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "oracle_fusion_cloud"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (7)

| Internal name | Title | Batch |
|---|---|---|
| `new_batch_object` | New record | yes |
| `new_business_event` | New business event | - |
| `new_employee_atom_feed_entry` | New employee atom feed entry | - |
| `new_object` | New record | - |
| `new_organization_atom_feed_entry` | New organization atom feed entry | - |
| `updated_batch_object` | New/updated record | yes |
| `updated_object` | New/updated record | - |


## Actions (28)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `advanced_search_object` | Search records using advanced query | yes |
| `append_file_comment` | Append file comment | - |
| `confirm_extract_consumption` | Confirm extract consumption | - |
| `create_object` | Create record | - |
| `create_object_batch` | Create records | yes |
| `create_user` | Create user | - |
| `delete_object` | Delete record | - |
| `download_ess_job_execution_details` | Download ESS job execution details | - |
| `download_export_output` | Download export output | - |
| `export_bulk_data` | Export bulk data | - |
| `extract_and_purge` | Extract and purge | - |
| `fetch_extract_output` | Fetch extract output | - |
| `flow_task_instance_status` | Get flow task instance status | - |
| `get_object` | Get record | - |
| `import_bulk_data` | Import bulk data | - |
| `list_entities` | List entities | - |
| `load_and_import_data` | Load and import data | - |
| `search_documents_for_file_prefix` | Search documents by file prefix | - |
| `search_object` | Search records | yes |
| `submit_and_get_flow_instance_id` | Submit and get flow instance ID | - |
| `submit_ess_job_request` | Submit ESS job request | - |
| `submit_job_with_output` | Submit job with output | - |
| `update_interface_data` | Update interface data | - |
| `update_object` | Update record | - |
| `update_object_batch` | Update records | yes |
| `upload_to_ucm` | Upload to UCM | - |
| `upsert_object` | Upsert record | - |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
