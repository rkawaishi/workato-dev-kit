# Amazon SQS コネクタ

Provider: `aws_sqs`

## Triggers

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| New message | `new_message` | - |  |
| New messages | `new_messages_batch` | Yes |  |

## Actions

| 名前 | provider 内名称 | Batch | 説明 |
|---|---|---|---|
| Delete message | `delete_message` | - |  |
| Delete messages | `delete_messages_batch` | Yes |  |
| Receive message | `receive_message` | - |  |
| Send message | `send_message` | - |  |
| Send messages | `send_messages_batch` | Yes |  |
