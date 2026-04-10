# Zuora コネクタ

Provider: `zuora`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New/updated order | `new_updated_order` | - |  |
| New/updated record | `new_updated_record` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create custom record | `create_custom_object` | Yes |  |
| Create record | `create_record` | - |  |
| Get custom record | `get_custom_object_record` | - |  |
| Get record | `get_object` | - |  |
| Get order by order number | `get_order` | Yes |  |
| Get orders by subscription number | `get_subscriptions` | - |  |
| Query records | `query_records` | Yes |  |
| Search records | `search_records` | Yes |  |
| Update custom record | `update_custom_object` | Yes |  |
| Update order trigger date | `update_order_triggerdate` | - |  |
| Update record | `update_record` | - |  |
