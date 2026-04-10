# SAP OData コネクタ

Provider: `sap_s4_hana_cloud`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New object | `new_object` | - |  |
| Updated object | `new_or_updated_object` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Batch request | `batch_request` | Yes |  |
| Create object | `create_object` | - |  |
| Delete object | `delete_object` | - |  |
| Get object details by ID | `get_object` | - |  |
| Search object | `search_object` | Yes |  |
| Extract bulk data | `search_object_with_proxy` | - |  |
| Update object | `update_object` | - |  |
| Upsert object | `upsert_object` | - |  |
