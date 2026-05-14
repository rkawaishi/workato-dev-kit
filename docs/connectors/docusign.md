# DocuSign connector

Provider: `docusign`

## Triggers

| Name | Internal name | Batch | Description |
|---|---|---|---|
| New document received | `new_document_received` | - |  |
| New document event | `new_event` | - |  |
| New recipient event | `new_recipient_event` | - |  |
| New signed document | `new_signed_document` | - |  [deprecated] |

## Actions

| Name | Internal name | Batch | Description |
|---|---|---|---|
| Custom action | `__adhoc_http_action` | - |  |
| Create/send document | `create_envelope` | - |  |
| Download document | `download_document` | - |  |
| List documents in envelope | `list_documents` | Yes |  |
| Send document using a template | `send_envelope` | - |  |
