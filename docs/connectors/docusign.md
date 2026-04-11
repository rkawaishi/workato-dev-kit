# DocuSign コネクタ

Provider: `docusign`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New document received | `new_document_received` | - |  |
| New document event | `new_event` | - |  |
| New recipient event | `new_recipient_event` | - |  |
| New signed document | `new_signed_document` | - |  [deprecated] |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create/send document | `create_envelope` | - |  |
| Download document | `download_document` | - |  |
| List documents in envelope | `list_documents` | Yes |  |
| Send document using a template | `send_envelope` | - |  |
