# Zuora connector

Provider: `zuora`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New/updated order | `new_updated_order` | - |  |
| New/updated record | `new_updated_record` | - |  |

## Actions

| Name | Internal name | Batch | Description |
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
