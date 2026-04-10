# Tradeshift コネクタ

Provider: `tradeshift`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Credit note ready | `credit_note_ready` | - |  |
| Invoice ready | `invoice_ready` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create chart of accounts | `create_code` | - |  |
| Create Credit note | `create_credit_note` | - |  |
| Create external connection | `create_external_connection` | - |  |
| Create Invoice | `create_invoice` | - |  |
| Delete chart of accounts | `delete_coding_list` | - |  |
| Get current account info | `get_account_info` | - |  |
| Search connections | `search_connections` | Yes |  |
| Tag document | `tag_document` | - |  |
| Untag document | `untag_document` | - |  |
| Update connection properties | `update_connection_properties` | - |  |
