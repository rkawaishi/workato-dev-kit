# Salesforce secondary コネクタ

Provider: `salesforce_secondary`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Monitor changes in a record | `change_data_capture` | - |  |
| Case is closed | `closed_case` | - |  [deprecated] |
| Campaign is completed | `completed_campaign` | - |  [deprecated] |
| Account created | `new_account` | - |  [deprecated] |
| Campaign created | `new_campaign` | - |  [deprecated] |
| Campaign member created | `new_campaign_member` | - |  [deprecated] |
| Case created | `new_case` | - |  [deprecated] |
| Contact created | `new_contact` | - |  [deprecated] |
| New record | `new_custom_object` | - |  |
| New record | `new_custom_object_webhook` | - |  |
| New duplicate record item | `new_duplicate_record_item` | - |  [deprecated] |
| Duplicate record set created | `new_duplicate_record_set` | - |  [deprecated] |
| Lead created | `new_lead` | - |  [deprecated] |
| Note created | `new_note` | - |  [deprecated] |
| Opportunity created | `new_opportunity` | - |  [deprecated] |
| New Outbound message | `new_outbound_message` | - |  |
| New platform event | `new_platform_event` | - |  |
| New PushTopic event | `new_pushtopic_event` | - |  |
| Export new records | `scheduled_sobject_bulk_v2_created` | - |  |
| Export new/updated records | `scheduled_sobject_bulk_v2_created_or_updated` | - |  |
| Scheduled record search using SOQL query WHERE clause | `scheduled_sobject_soql_query` | Yes |  |
| Scheduled records search using SOQL query | `scheduled_sobject_soql_query_v2` | Yes |  |
| New records | `sobject_batch_created` | Yes |  |
| New/updated records | `sobject_batch_created_or_updated` | Yes |  |
| Threshold met for new records created | `sobject_created_bulk` | Yes |  |
| Deleted record | `sobject_deleted` | - |  |
| Account created/updated | `updated_account` | - |  [deprecated] |
| Campaign created/updated | `updated_campaign` | - |  [deprecated] |
| Campaign member created/updated | `updated_campaign_member` | - |  [deprecated] |
| Case created/updated | `updated_case` | - |  [deprecated] |
| Contact created/updated | `updated_contact` | - |  [deprecated] |
| New/updated record | `updated_custom_object` | - |  |
| New/updated record | `updated_custom_object_webhook` | - |  |
| Lead created/updated | `updated_lead` | - |  [deprecated] |
| Note created/updated | `updated_note` | - |  [deprecated] |
| Opportunity created/updated | `updated_opportunity` | - |  [deprecated] |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Approve record in approval process | `approve_process` | - |  |
| Create records in bulk | `bulk_insert_sobject` | Yes |  [deprecated] |
| Update records in bulk | `bulk_update_sobject` | Yes |  [deprecated] |
| Upsert records in bulk | `bulk_upsert_sobject` | Yes |  [deprecated] |
| Create records in batches | `composite_create_sobject` | Yes |  |
| Update records in batches | `composite_update_sobject` | Yes |  |
| Create account | `create_account` | - |  [deprecated] |
| Create campaign | `create_campaign` | - |  [deprecated] |
| Add campaign member to campaign | `create_campaign_member` | - |  [deprecated] |
| Create case | `create_case` | - |  [deprecated] |
| Create contact | `create_contact` | - |  [deprecated] |
| Create record | `create_custom_object` | - |  |
| Publish platform event | `create_custom_platform_event` | - |  |
| Create lead | `create_lead` | - |  [deprecated] |
| Create note | `create_note` | - |  [deprecated] |
| Create opportunity | `create_opportunity` | - |  [deprecated] |
| Delete record | `delete_sobject` | - |  |
| Get account details | `get_account` | - |  [deprecated] |
| Download attachment | `get_attachment_body` | - |  |
| Get campaign details | `get_campaign` | - |  [deprecated] |
| Get campaign member details | `get_campaign_members` | - |  [deprecated] |
| Download file | `get_combined_attachment` | - |  |
| Get contact details | `get_contact` | - |  [deprecated] |
| Get record details by ID | `get_custom_object` | - |  |
| Get document by ID | `get_document` | - |  [deprecated] |
| Get lead details | `get_lead` | - |  [deprecated] |
| Get opportunity details | `get_opportunity` | - |  [deprecated] |
| Get related list by parent record ID | `get_related` | Yes |  |
| Get report by ID | `get_report_by_id` | - |  |
| Get object schema | `get_sobject_schema` | - |  |
| Create records in bulk from CSV file | `insert_bulk_job` | - |  |
| Create records in bulk from CSV file (API 1.0) | `insert_bulk_job_v1` | - |  |
| List data category groups | `list_data_category_groups` | Yes |  |
| List reports | `list_reports` | - |  [deprecated] |
| Search accounts | `lookup_account` | - |  [deprecated] |
| Search campaigns | `lookup_campaign` | - |  [deprecated] |
| Search contacts | `lookup_contact` | - |  [deprecated] |
| Search leads | `lookup_lead` | - |  [deprecated] |
| Search opportunities | `lookup_opportunity` | - |  [deprecated] |
| Retrieve data category group hierarchy | `read_data_category_group` | Yes |  |
| Reject record in approval process | `reject_process` | - |  |
| Retry bulk job for failed records from CSV file | `retry_bulk_jobs` | - |  |
| Search records | `search_sobjects` | Yes |  |
| Search records using SOQL query WHERE clause | `search_sobjects_soql` | Yes |  |
| Search records in bulk using SOQL query (API 1.0) | `search_sobjects_soql_bulk_csv` | - |  |
| Search records in bulk using SOQL query (API 2.0) | `search_sobjects_soql_bulk_csv_v2` | - |  |
| Search records using SOQL query | `search_sobjects_soql_v2` | Yes |  |
| Submit record for approval | `submit_process` | - |  |
| Update account | `update_account` | - |  [deprecated] |
| Update records in bulk from CSV file | `update_bulk_job` | - |  |
| Update records in bulk from CSV file (API 1.0) | `update_bulk_job_v1` | - |  |
| Update campaign | `update_campaign` | - |  [deprecated] |
| Update opportunity | `update_opportunity` | - |  [deprecated] |
| Update record | `update_sobject` | - |  |
| Upload file | `upload_file_content` | - |  |
| Upsert records in bulk from CSV file | `upsert_bulk_job` | - |  |
| Upsert records in bulk from CSV file (API 1.0) | `upsert_bulk_job_v1` | - |  |
| Upsert records in batches | `upsert_composite_sobject` | Yes |  |
| Upsert record | `upsert_sobject` | - |  |
