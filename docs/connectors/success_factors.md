# SAP SuccessFactors OData コネクタ

Provider: `success_factors`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New or updated object | `new_updated_object` | - |  |
| New or updated objects in batch | `new_updated_object_batch` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Search records using OData query | `advance_search_object` | Yes |  |
| Create record | `create_object` | - |  |
| Get record details | `get_object` | - |  |
| Merge record | `merge_object` | - |  |
| Search records | `search_object` | Yes |  |
| Update record | `update_object` | - |  |
| Upsert records (single object) | `upsert_object` | Yes |  |
| Upsert record | `upsert_record_object` | - |  |
| Upsert records (multiple objects) | `upsert_records_transactional` | Yes |  |
