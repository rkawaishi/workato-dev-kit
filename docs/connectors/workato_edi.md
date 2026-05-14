# Workato EDI connector

Provider: `workato_edi`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New transactions in bucket | `new_transactions_in_polling_bucket` | - |  |

## Actions

| Name | Internal name | Batch | Description |
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
