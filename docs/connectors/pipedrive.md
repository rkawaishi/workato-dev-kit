# Pipedrive コネクタ

Provider: `pipedrive`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New object | `added_object` | - |  |
| New deal | `new_deal` | - |  [deprecated] |
| New or Updated object | `updated_object` | - |  |
| New or updated object | `updated_object_batch` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create activity | `create_activity` | - |  |
| Create deal | `create_deal` | - |  |
| Create note | `create_note` | - |  |
| Create organization | `create_organization` | - |  |
| Get deal related products | `get_deal_related_products` | Yes |  |
| Get object | `get_object` | Yes |  |
| Update deal | `update_deal` | - |  |
| Update organization | `update_organization` | - |  |
| Update person | `update_person` | - |  |
