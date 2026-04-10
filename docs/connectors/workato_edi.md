# Workato EDI コネクタ

Provider: `workato_edi`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New transactions in bucket | `new_transactions_in_polling_bucket` | - |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Approve delivery | `approve_delivery` | - |  [deprecated] |
| Convert data format | `convert_data_format` | - |  |
| Create record | `create_record` | - |  |
| Fail delivery | `fail_delivery` | - |  [deprecated] |
| Generate label | `generate_label` | - |  |
| Get record | `get_record` | - |  |
| List transactions from polling bucket | `list_transactions_from_polling_bucket` | Yes |  [deprecated] |
| Search records | `search_records` | Yes |  |
