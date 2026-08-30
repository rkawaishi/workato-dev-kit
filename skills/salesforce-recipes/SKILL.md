# Salesforce recipes

Provider value to use in every step: `salesforce`

This skill extends the base `workato-recipes` skill. Read that first for recipe JSON structure, datapill syntax, and control flow; this document only covers what is specific to this connector.

## Before you generate

- Set `"provider": "salesforce"` on every step that uses this connector.
- Use only the internal names listed below. They are the same list `lint-rules.json` enforces, so anything else fails `wk lint`.
- Reach for `__adhoc_http_action` only when no native operation covers the call.

## Triggers (16)

| Internal name | Title | Batch |
|---|---|---|
| `change_data_capture` | Monitor changes in a record | - |
| `new_custom_object` | New record | - |
| `new_custom_object_webhook` | New record | - |
| `new_outbound_message` | New Outbound message | - |
| `new_platform_event` | New platform event | - |
| `new_pushtopic_event` | New PushTopic event | - |
| `scheduled_sobject_bulk_v2_created` | Export new records | - |
| `scheduled_sobject_bulk_v2_created_or_updated` | Export new/updated records | - |
| `scheduled_sobject_soql_query` | Scheduled record search using SOQL query WHERE clause | yes |
| `scheduled_sobject_soql_query_v2` | Scheduled records search using SOQL query | yes |
| `sobject_batch_created` | New records | yes |
| `sobject_batch_created_or_updated` | New/updated records | yes |
| `sobject_created_bulk` | Threshold met for new records created | yes |
| `sobject_deleted` | Deleted record | - |
| `updated_custom_object` | New/updated record | - |
| `updated_custom_object_webhook` | New/updated record | - |


## Actions (33)

| Internal name | Title | Batch |
|---|---|---|
| `__adhoc_http_action` | Custom action | - |
| `approve_process` | Approve record in approval process | - |
| `composite_create_sobject` | Create records in batches | yes |
| `composite_update_sobject` | Update records in batches | yes |
| `create_custom_object` | Create record | - |
| `create_custom_platform_event` | Publish platform event | - |
| `delete_sobject` | Delete record | - |
| `get_attachment_body` | Download attachment | - |
| `get_combined_attachment` | Download file | - |
| `get_custom_object` | Get record details by ID | - |
| `get_related` | Get related list by parent record ID | yes |
| `get_report_by_id` | Get report by ID | - |
| `get_sobject_schema` | Get object schema | - |
| `insert_bulk_job` | Create records in bulk from CSV file | - |
| `insert_bulk_job_v1` | Create records in bulk from CSV file (API 1.0) | - |
| `list_data_category_groups` | List data category groups | yes |
| `read_data_category_group` | Retrieve data category group hierarchy | yes |
| `reject_process` | Reject record in approval process | - |
| `retry_bulk_jobs` | Retry bulk job for failed records from CSV file | - |
| `search_sobjects` | Search records | yes |
| `search_sobjects_soql` | Search records using SOQL query WHERE clause | yes |
| `search_sobjects_soql_bulk_csv` | Search records in bulk using SOQL query (API 1.0) | - |
| `search_sobjects_soql_bulk_csv_v2` | Search records in bulk using SOQL query (API 2.0) | - |
| `search_sobjects_soql_v2` | Search records using SOQL query | yes |
| `submit_process` | Submit record for approval | - |
| `update_bulk_job` | Update records in bulk from CSV file | - |
| `update_bulk_job_v1` | Update records in bulk from CSV file (API 1.0) | - |
| `update_sobject` | Update record | - |
| `upload_file_content` | Upload file | - |
| `upsert_bulk_job` | Upsert records in bulk from CSV file | - |
| `upsert_bulk_job_v1` | Upsert records in bulk from CSV file (API 1.0) | - |
| `upsert_composite_sobject` | Upsert records in batches | yes |
| `upsert_sobject` | Upsert record | - |


## Deprecated -- do not generate

Workato still executes these in existing recipes, but new recipes must not use them. They are excluded from `valid_action_names`.


### Triggers

| Internal name | Title | Batch |
|---|---|---|
| `closed_case` | Case is closed | - |
| `completed_campaign` | Campaign is completed | - |
| `new_account` | Account created | - |
| `new_campaign` | Campaign created | - |
| `new_campaign_member` | Campaign member created | - |
| `new_case` | Case created | - |
| `new_contact` | Contact created | - |
| `new_duplicate_record_item` | New duplicate record item | - |
| `new_duplicate_record_set` | Duplicate record set created | - |
| `new_lead` | Lead created | - |
| `new_note` | Note created | - |
| `new_opportunity` | Opportunity created | - |
| `updated_account` | Account created/updated | - |
| `updated_campaign` | Campaign created/updated | - |
| `updated_campaign_member` | Campaign member created/updated | - |
| `updated_case` | Case created/updated | - |
| `updated_contact` | Contact created/updated | - |
| `updated_lead` | Lead created/updated | - |
| `updated_note` | Note created/updated | - |
| `updated_opportunity` | Opportunity created/updated | - |


### Actions

| Internal name | Title | Batch |
|---|---|---|
| `bulk_insert_sobject` | Create records in bulk | yes |
| `bulk_update_sobject` | Update records in bulk | yes |
| `bulk_upsert_sobject` | Upsert records in bulk | yes |
| `create_account` | Create account | - |
| `create_campaign` | Create campaign | - |
| `create_campaign_member` | Add campaign member to campaign | - |
| `create_case` | Create case | - |
| `create_contact` | Create contact | - |
| `create_lead` | Create lead | - |
| `create_note` | Create note | - |
| `create_opportunity` | Create opportunity | - |
| `get_account` | Get account details | - |
| `get_campaign` | Get campaign details | - |
| `get_campaign_members` | Get campaign member details | - |
| `get_contact` | Get contact details | - |
| `get_document` | Get document by ID | - |
| `get_lead` | Get lead details | - |
| `get_opportunity` | Get opportunity details | - |
| `list_reports` | List reports | - |
| `lookup_account` | Search accounts | - |
| `lookup_campaign` | Search campaigns | - |
| `lookup_contact` | Search contacts | - |
| `lookup_lead` | Search leads | - |
| `lookup_opportunity` | Search opportunities | - |
| `update_account` | Update account | - |
| `update_campaign` | Update campaign | - |
| `update_opportunity` | Update opportunity | - |


## Field details

Input/output field definitions observed from the Workato UI. The Workato API does not expose these, so treat them as the authoritative source for required fields and types.

### search_sobjects (Action)

Recipe: Search Contracts in Salesforce

Input and output schemas are not configured (dynamically determined after Connection).

> **Note:** This step has `input: {}` (empty), so the object type and fields are dynamically generated after the Salesforce Connection is configured.

---

### update_sobject (Action)

Recipe: Update Contract in Salesforce

Input and output schemas are not configured (dynamically determined after Connection).

> **Note:** This step has `input: {}` (empty), so the object type and fields are dynamically generated after the Salesforce Connection is configured.

#### Related Genie parameters (start_workflow trigger)

Search Contracts Recipe:

| Field | Type | Required | Description |
|---|---|---|---|
| contract_name | string | Yes | the name of the contract which user is referencing |
| contract_content | string | Yes | contents of the contract which user is referencing |

Update Contract Recipe:

| Field | Type | Required | Description |
|---|---|---|---|
| contract_name | string | Yes | Contract name |
| contract_content | string | - | Contract content |

#### Genie Result Schema

| Field | Type | Required | Description |
|---|---|---|---|
| response | string | Yes | Response |


## Validation

```bash
wk lint <recipe>.recipe.json --skills-path <path-to>/skills
```
